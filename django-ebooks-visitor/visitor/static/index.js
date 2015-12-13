//AngularJS Model
//function DisplayCtrl($scope) {
//    $scope.mainAppText = 'This is main app text';
//
//}

var app = angular.module('app', []);

app.config(function ($sceProvider) {
	// Completely disable SCE.  For demonstration purposes only!
	// Do not use in new projects.
	$sceProvider.enabled(false);
});

app.controller('DisplayController', function ($scope, $http) {

	//Display Management
	$scope.updateDisplay = function (pageSerial, searchWords) {
		if (pageSerial === undefined) {
			pageSerial = 1;
		}
		$http.get("page?pageSerial=" + pageSerial).
			success(function (response) { //data, status, headers, config
				var result = utils.highlight(response, searchWords);
				result = utils.processNewLines(result);
				result = result.replace(/href="([^"]+)"/g,
					'href onclick="onHandleDisplayLinkClick(\'$1\')"');
				$scope.mainAppText = result;
				$scope.pageSerial = pageSerial;
				location.hash = pageSerial;
			});
	};

	//This one is called sloely from Mogama and headless TOC
	$scope.displayHome = function () {
		//var pageSerial = $scope.pageSerial;
		var pageSerial = 1;
		$scope.updateDisplay(pageSerial);
		var tocCurTopicId = 1;
		$scope.updateTOC(tocCurTopicId);
	};

	$scope.displayNext = function () {
		var pageSerial = $scope.pageSerial;
		pageSerial++;
		$scope.updateDisplay(pageSerial);
		$scope.updateTOCBySerial(pageSerial)

	};

	$scope.displayPrevious = function () {
		var pageSerial = $scope.pageSerial;
		if (pageSerial - 1 < 1) {
			return;
		}
		pageSerial--; //automatic conversion to integer
		$scope.updateDisplay(pageSerial);
		$scope.updateTOCBySerial(pageSerial)
	};

	$scope.displayFromToc = function (pageSerial) {
		$scope.updateDisplay(pageSerial);
		$("#right-panel").panel("close");
	};

	$scope.displayFromIndexHits = function (pageSerial) {
		$("#left-panel").panel("close");
		$scope.updateDisplay(pageSerial);
		$scope.updateTOCBySerial(pageSerial)
	};

	$scope.displayFromSearch = function (pageSerial, searchWords) {
		$scope.updateDisplay(pageSerial, searchWords);
		$scope.updateTOCBySerial(pageSerial);
		$("#left-panel").panel("close");
	};

	$scope.displaySearchByNum = function (pageSerial) {
		$scope.updateDisplay(pageSerial);
		$scope.updateTOCBySerial(pageSerial)
	};


//TOC Management
	$scope.updateTOC = function (curTopicId) {
		$http.get("topics?topic=" + curTopicId).
			success(function (response) { //data, status, headers, config
				//$scope.tocCurTopicId = curTopicId;
				$scope.tocTree = response;
				setTocHitsHeight();
			});
	};

	$scope.updateTOCBySerial = function (serialNo) {
		$http.get("topics?serial=" + serialNo).
			success(function (response) { //data, status, headers, config
				//$scope.tocCurTopicId = curTopicId;
				$scope.tocTree = response;
				setTocHitsHeight();
			});
	};

	$scope.getSpaces = function (n) {
		return utils.getSpaces(n);
	};

//Indexes Management
	$scope.loadIndexHits = function (indexType, arrayIndex) {
		$http.get("fehres?type=" + indexType).
			success(function (response) { //data, status, headers, config
				$scope.indexes[arrayIndex]['hits'] = response;
			});
	};

	$scope.selectedIndexChanged = function () {
		var arrayIndex = parseInt($scope.curIndex.sort);
		if ($scope.indexes[arrayIndex].hits == "0") {
			$scope.loadIndexHits($scope.curIndex.type, arrayIndex);
		}
		$scope.indexItemHits = "";
	};

	$scope.updateIndexItemHits = function (indexType, id) {
		$http.get("fehresPages?type=" + indexType + "&id=" + id).
			success(function (response) { //data, status, headers, config
				$scope.indexItemHits = response;
			});
	};

//Search Management
	$scope.updateSearchHits = function () {
		if ($scope.searchWords.length == 0) {
			return;
		}
		setSearchHitsHeight();
		$.mobile.loading("show");//hourglass
		console.log($scope.searchOption);
		var url = "search?word=" + $scope.searchWords + "&page=" + $scope.searchCurPageNo +
							"&option=" + $scope.searchOption +
							"&all=1&exact=1&root=0&exclude=&ids=all&pages=all&mobile=y";
		$http.get(url).
			success(function (response) { //data, status, headers, config
				$scope.searchHits = response;
				$scope.searchPagesCount = Math.ceil(response.count / 10);
				$.mobile.loading("hide");//hourglass
			});
	};

	$scope.searchNext = function () {
		if ($scope.searchCurPageNo + 1 <= $scope.searchPagesCount) {
			$scope.searchCurPageNo += 1;
			$scope.updateSearchHits();
		}
	};

	$scope.searchPrevious = function () {
		if ($scope.searchCurPageNo - 1 > 0) {
			$scope.searchCurPageNo -= 1;
			$scope.updateSearchHits();
		}
	};

//User Management
	$scope.openLoginDialog = function () {
		$scope.email = $.cookie("family_email");
		$scope.errorMessage = "";
		$.mobile.changePage("#popup-dialog-login", {changeHash: false});
	};

	$scope.doLogin = function () {
		if ($scope.email.length == 0 || $scope.password.length == 0) {
			$scope.errorMessage = "خطأ في اسم المستخدم أو كلمة السر";
			return;
		}

		$http.get("../visitor/signin?email=" + $scope.email + "&password=" + $scope.password).
			success(function (response) { //data, status, headers, config
				if(response=="success") {
					$scope.errorMessage = "";
					$.cookie("family_email", $scope.email);
					$.cookie("family_loggedin", "true");
					$.mobile.changePage("#demo-page", {changeHash: false});
					$scope.isLoggedIn = true;
					$scope.loadBookmarksList();
					} else {
					$.cookie("family_is_loggedin", "");
					$scope.errorMessage = "خطأ في الدخول";
					//setLoggedInDirectly("");
					$scope.isLoggedIn = false;
					$('#bookmarks-table').empty();
				}
			}).
			error(function (data, status, headers, config) {
				$.cookie("family_is_loggedin", "");
				$scope.errorMessage = "خطأ في الدخول";
				//setLoggedInDirectly("");
				$scope.isLoggedIn = false;
				$('#bookmarks-table').empty();
			});
	};

	$scope.logout = function () {
		$.cookie("family_loggedin", ""); //clear logged in cookie
		$scope.isLoggedIn = false;
		$scope.email = "";
		$scope.password = "";
		$scope.bookmarks = [];

	};

	$scope.registerUser = function () {
		$scope.registerationError = "";
		var email = $scope.registerEmail;
		var password = $scope.registerPassword;
		var password2 = $scope.registerPassword2;
		if (!utils.validateEmail(email)) {
			$scope.registerationError = "البريد الإلكتروني غير سليم";
			return;
		}
		if (password !== password2) {
			$scope.registerationError = "كلمتي السر غير متطابقه";
			return;
		}
		if (password.length < 8) {
			$scope.registerationError = "كلمة السر قصيره، لا ينبغي أن يقل طول كلمة السر عن ٨ أحرف";
			return;
		}
		$http.get("../visitor/signup?email=" + email + "&password=" + password + "&password2=" + password2).
			success(function (response) { //data, status, headers, config
				if (response === 'success') {
					$.mobile.changePage("#demo-page", {changeHash: false});
					alert("تم التسجيل بنجاج");
					//store email so that, it will be easier to login
					$.cookie("family_email", email);
				} else {
					console.log('>Unable to register for ' + email);
					$scope.registerationError = "خطأ في التسجيل، برجاء تغيير البريد الالكتروني";
				}
			}).
			error(function (data, status, headers, config) {
				//No handling yet
			});
	};

//Bookmarks
	$scope.loadBookmarksList = function () {
		$http.get("../visitor/get_bookmarks?").
			success(function (response) { //data, status, headers, config
				$scope.bookmarks = response;
			});
	};

	$scope.deleteBookmark = function (clickedItem, bookmarkId) {
		console.log(clickedItem);
		$http.get("../visitor/del_bookmark?id=" + bookmarkId).
			success(function (result) {
				if (result === 'success') {
					//$('#' + bookmarkId).remove();
					//$scope.bookmarks
					$scope.loadBookmarksList();//reload
				}
			});
	};

	$scope.addNewDisplayBookmark = function () {
		var snippet = utils.shortenText(utils.stripHtml($scope.mainAppText), 8);
		var bookmarkID = utils.guid();
		var ajaxUrl = utils.strf("../visitor/set_bookmark?bookmark_id={0}&pageSerial={1}&title={2}",
			bookmarkID, $scope.pageSerial, encodeURIComponent(snippet));
		$http.get(ajaxUrl).
			success(function (result) {
				if (result === 'success') {
					$scope.loadBookmarksList(); //reload updated one
				} else {
					alert("خطأ في الإضافة");
				}
			});
	};

	$scope.linkToArticle = function (id) {
		$http.get("serial?topicId=" + id).
			success(function (result) {
				$scope.updateDisplay(result_obj.serial);
			});
	};

	$scope.displayDefinition = function (type, id) {
		$http.get("definition?type=" + type + "&id=" + id).
			success(function (result) {
				$scope.definition = result;
				//window.location.href = "#popup-dialog-def"; //show the dialogue
				$.mobile.changePage("#popup-dialog-def", {changeHash: false});

			});
	};

	$scope.updateMa3lama = function (id, pageNo) {
		$.mobile.changePage("#popup-dialog-ma3lama", {changeHash: false});
		$http.get("ma3lama_books?book=" + id + "&page=" + pageNo).
			success(function (result) {
				$scope.ma3lama = result;
				$scope.ma3lamaCurPage = pageNo;
			});
	};

	$scope.ma3lamaNext = function () {
		$scope.ma3lamaCurPage = Math.min($scope.ma3lamaCurPage + 1, $scope.ma3lama.max);
		$scope.updateMa3lama($scope.ma3lama.book, $scope.ma3lamaCurPage);
	};

	$scope.ma3lamaPrevious = function () {
		$scope.ma3lamaCurPage = Math.max($scope.ma3lamaCurPage - 1, 1);
		$scope.updateMa3lama($scope.ma3lama.book, $scope.ma3lamaCurPage);
	};

	//
	$scope.updateIndexNamesList = function () {
		$http.get("fehresList?").
			success(function (response) { //data, status, headers, config
				$scope.indexes = response;
				$scope.curIndex = $scope.indexes[0];
				console.log("Current Index= " + $scope.curIndex);
				$scope.selectedIndexChanged(); //Fill list of index hits initially
			});
	};

	//INITIALIZATION

	//Indexs Model
	setDisplayBoxHeight();
	setIndexHitsHeights();
	setBookmarksListHeight();
	$scope.searchOption = "or";//select the option initially
	$scope.updateIndexNamesList();

	//Search Model
	$scope.searchHits = {'count': 0, 'page_number': 1, 'results': []};
	$scope.searchCurPageNo = 1; // page_number
	$scope.searchPagesCount = 0;

	//MAIN DISPLAY
	$scope.isLoggedIn = false;
	if ($.cookie("family_loggedin") === "true") {
		$scope.isLoggedIn = true;
		$scope.loadBookmarksList();
		$scope.email = $.cookie("family_email");
	}

	//Display
	var hash = location.hash;
	var pageSerial;
	if (hash && hash.length > 0) {
		pageSerial = hash.substr("1");
	} else {
		pageSerial = "1";
	}
	$scope.updateDisplay(pageSerial);
	var topicId = 1;
	$scope.updateTOC(topicId);

	var title = uiStrings['shortTitle'];
	if ($(window).width() >= 800) { //Desktop sizing: visible left panel the whole time
		title = uiStrings['longTitle'];
	}
	$scope.appTitle = title;
	$scope.appTitleShort = uiStrings['shortTitle'];

});


// SWIPE Support for touch screens
$(document).on("pagecreate", "#demo-page", function () {

	if ($(window).width() > 800) {
		return; //NO SWIP SUPPORT
	}

	$(document).on("swipeleft swiperight", "#demo-page", function (e) {
		// We check if there is no open panel on the page because otherwise
		// a swipe to close the left panel would also open the right panel (and v.v.).
		// We do this by checking the data that the framework stores on the page element (panel: open).
		var displayCont = angular.element($('#main-body-tag')).scope();

		if ($(".ui-page-active").jqmData("panel") !== "open") {
			if (e.type === "swipeleft") {
//                 $("#right-panel").panel("open");
				displayCont.displayPrevious();
			} else if (e.type === "swiperight") {
//                $("#left-panel").panel("open");
				displayCont.displayNext();
			}
			displayCont.$apply(); //if anything is updated
		}
	});
});

$(document).ready(function(){

	//var closeBox = document.querySelector("#popup-dialog-register div div a");
	//if (closeBox) {
	//	//delete closeBox.href;
	//	//delete closeBox['data-rel'];
	//	//closeBox.href = "";
	//	closeBox.onclick = function () {
	//		$.mobile.changePage("#demo-page", {changeHash: false});
	//	};
	//}


});

//Definition handling, modified
function onHandleDisplayLinkClick(tag) {
	//var thisView = this;
	//TermALAM-id-24-join-3     aalam
	//TermMost-id-24-join-3     mostala7at
	//MT-id-1192-join-31        mawad
	//BR-id-2-join-32           kotob
	//ML-id-2-join3             qawa3ed
	//(2)555                    hamesh

	tag = decodeURI(tag);
	if (tag[0] == '(') { // hamesh
		scrollToBottom();
		return;
	}

	// fahares
	var tagParts = tag.split("-");
	var type = tagParts[0];
	var id = tagParts[2];
	var displayCont = angular.element($('#main-body-tag')).scope();

	if (type == "MT") { //mawad
		displayCont.linkToArticle(id);
	}
	else if (type == "ML") { //Empty by Tharwat !!!
		//alert(id);
		displayCont.updateMa3lama(id, 1);
	}
	else { //showing popup dialogue
		displayCont.displayDefinition(type, id);
	}
	displayCont.$apply(); //if anything is updated

}

function scrollToBottom() {
	$(document).scrollTop($(document).height());
}

function openRegisterDialog() {
	$.mobile.changePage(
		"#popup-dialog-register", {changeHash: false});
}

function openDialog(dlgId) {
	$.mobile.changePage(dlgId, {changeHash: false});
}
//
//Not used

//Dynamic Sizes

function setIndexHitsHeights() {
	var indexHeight = $(window).height() - $("#tabs-header").height() -
		($("#select-menu-indexes").height() * 3); //for the filter box and other spaces
	if ($(window).width() >= 800) { //Desktop sizing: visible left panel the whole time
		indexHeight = indexHeight - $(".demo-page-top-header").height() - 30;
	}
	var height1 = indexHeight * 2 / 3;
	$('.scrollable-table-index').css('max-height', height1 + 'px');
	console.log("Index hits height: " + indexHeight);

	//resize index-hit-hits
	var height2 = indexHeight * 2 / 3;
	$('#index-hit-hits').css('max-height', height2 + 'px');

}

function setSearchHitsHeight() {
	var searchHitsHeight = $(window).height() - ($("#search-button").height() * 15); //
	if ($(window).width() >= 800) {
		searchHitsHeight -= $(".demo-page-top-header").height();
	}
	console.log("Search hits height: " + searchHitsHeight);
	$('.scrollable-table').css('max-height', searchHitsHeight + 'px');
}

function setTocHitsHeight() {
	var height = $(window).height() - $("#toc-separator").position().top;
	if ($(window).width() >= 800) {
		height = height - $(".demo-page-top-header").height() - 10;
	}
	$('.scrollable-table-toc').css('max-height', height + 'px');
	console.log(">TOC hits height: " + height);
}

function setBookmarksListHeight() {
	var height = $(window).height() - $("#tabs-header").height();
	if ($(window).width() >= 800) {
		height = height - $(".demo-page-top-header").height() - 10;
	}
	$('.scrollable-table-bookmarks').css('max-height', height + 'px');
}

function setDisplayBoxHeight() {
	var height = $(window).height() - $(".demo-page-top-header").height() - 50;
	$('.main-app-text-container').css('max-height', height + 'px');
}

//Whenever a history change in the same document
//window.onpopstate = function (event) {
//	var doSomething = "121";
//};

// Why I need this if at all: When I change the hash, the browser history is updated. But
// when I click back, the browser tell me through the below event but not update the display
// itself. This is why I made the below event handler
window.onhashchange = function () {
	//if (event && event.state && event.state.hash) {
	console.log("hash location changed: " + location.hash);
	var displayCont = angular.element($('#main-body-tag')).scope();

	if (location.hash.length > 0 && location.hash.indexOf("#popup-") == -1) { //if it is not a dialogue popup
		var url = location.hash;
		var pageSerial = url.substr("1");
		//The following condition is necessary to avoid double updating the page because of
		//changing the hash after update. It make a problem when displaying highlighed text
		//that came for search.
		if(displayCont.pageSerial == pageSerial) {
			console.log("No need to update page again!");
			return;
		}
		displayCont.updateDisplay(pageSerial);
		displayCont.$apply(); //if anything is updated
	}
};

function doCancelDialogue() {
	$.mobile.changePage("#demo-page", {changeHash: false});
}

//TODO Minify as the files are really getting very big, over 700 line of code
//TODO Move fonts into images folder

//
//window.onpopstate = function () {
//	//alert("Back/Forward clicked!");
//	var displayCont = angular.element($('#main-body-tag')).scope();
//
//	var params = utils.fillQueryParameters();
//	var initialPage = params['pageSerial'];
//	displayCont.updateDisplay(initialPage);
//	displayCont.$apply(); //if anything is updated
//
//};

//function openRightPanel() {
//	if ($("#right-panel").find("div").css("visibility") == "hidden") {
//		$("#right-panel").panel("close");
//	} else {
//		$("#right-panel").panel("open");
//	}
//}


//$( "#search-index-tab" ).tabs( "option", "active", 2 );

function setLoggedInDirectly(loggedIn) {
	if ("true" === loggedIn) {
		$("#logged-in-span").show();
		$("#logout-btn").show();
		$("#user-not-logged-in-span").hide();
		$("#hello-user").show();
		//$("#hello-user").empty();
		var db_index = queries['db'];
		var email = $.cookie(getEmailKey());
		$("#hello-user").text("مرحبا " + email);
		loadBookmarksList();
		console.log("Logged In State");
	} else {
		$("#logged-in-span").hide();
		$("#logout-btn").hide();
		$("#user-not-logged-in-span").show();
		//$("#hello-user").empty();
		$("#hello-user").hide();
		$('#bookmarks-table').empty();
		console.log("NOT Logged In State");
	}
}
//