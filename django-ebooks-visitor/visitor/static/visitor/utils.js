"use strict";

//Singleton Class
var utils = new function () {
//function Utils () {

	this.getSpaces = function (n) {
		//n = n * 1;
		var spaces = "";
		for (var i = 0; i < n; i++) {
			spaces += "&nbsp;";
		}
		return spaces
	};

	this.validator = function () {
		var invalid = "abcdefghijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()+=-[]\\\';,./{}|\":<>?";
		for (var i = 0; i < invalid.length; ++i)
			if (value.indexOf(invalid[i]) >= 0)
				return 'يسمح فقط بالحروف العربية';
	};

	this.validateEmail = function (email) {
		var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
		return re.test(email);
	};

	this.guid = function () {
		var d = new Date().getTime();
		return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
			var r = (d + Math.random() * 16) % 16 | 0;
			d = Math.floor(d / 16);
			return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
		});
		//return uuid;
	};

	//Example: var link = String.format('<a href="{0}/{1}/{2}" title="{3}">{3}</a>', url, year, titleEncoded, title);
	this.strf = function () {
		// The string containing the format items (e.g. "{0}")
		// will and always has to be the first argument.
		var theString = arguments[0];
		// start with the second argument (i = 1)

		//    for(var i in allImgs)
		for (var i = 1; i < arguments.length; i++) {
			// "gm" = RegEx options for Global search (more than one instance)
			// and for Multiline search
			var regEx = new RegExp("\\{" + (i - 1) + "\\}", "gm");
			theString = theString.replace(regEx, arguments[i]);
		}
		return theString;
	};

	this.replaceAll = function (string, find, replace) {
		//    return string.replace(new utils.RegExp(escapeRegExp(find), 'g'), replace);
		return string.replace(new RegExp(find, 'g'), replace);
	};

	this.escapeRegExp = function (string) {
		return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
	};

	this.shortenText = function (text, wordsCount) {
		//    var wordArray = text.split(' ').slice(0,wordsCount).join(' ');
		var wordArray = text.split(' ');
		if (wordArray.length <= wordsCount) {
			return text; //no shortening needed
		}
		var newText = wordArray.slice(0, wordsCount).join(' ');
		return newText + " ...";
	};

	this.stripHtml = function (htmlText) {
		return $(htmlText).text();
		//    return text.replace(/<\/?[^>]+(>|$)/g, "");
	};

	this.fillQueryParameters = function () {
		var vars = [], hash;
		var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
		for (var i = 0; i < hashes.length; i++) {
			hash = hashes[i].split('=');
			vars.push(hash[0]);
			vars[hash[0]] = hash[1];
		}
		return vars;

	};

	this.processNewLines = function (result) {
		result = utils.replaceAll(result, "\\\\@\\\\@", "<br>");
		result = utils.replaceAll(result, "\\\\@", "<br>");
		result = utils.replaceAll(result, "\\n", "<br>");
		return result;
	};

	//Highlight exact word, can not highlight vowel word using un-vowel word
	//this.highlight = function (text, searchWords) {
	//	if (searchWords !== undefined) {
	//		console.log('>Coloring search words');
	//		searchWords = searchWords.split(',');
	//		var spanStart = '<span class="highlight">';
	//		var spanEnd = '</span>';
	//		for (var i = 0; i < searchWords.length; ++i) {
	//			text = utils.replaceAll(text, searchWords[i], spanStart + searchWords[i] + spanEnd);
	//		}
	//	}
	//	return text;
	//};


	//This is a groups of boundary characters. \\ is escaping character; + means 1 or more
	var wordBoundary = '[ ;:,،.«»\'\"\\(\\)\\-\\{\\}\\<\\>]+';

	this.processArabicWord = function (arabic, wordBoundry) {
		var result = '';
		//unicode diacritics letters from url: http://unicode.org/charts/PDF/U0600.pdf
		var vowels = "[\u064B-\u065F]*"; //one or more vowel character

		for (var i = 0; i < arabic.length; i++) {
			result += arabic[i] + vowels;
		}
		//Insert word boundary mark
		//result = "\b" + result + "\b"; // DOES NOT WORK properly with ARABIC
		if (wordBoundry == true) {
			result = wordBoundary + result + wordBoundary;
		}
		console.log("search for, " + result);
		return result;
	};

	this.highlight = function (bodyString, searchWords) {
		if (searchWords === undefined) {
			return bodyString;
		}
		//Because of word boundary problem, I have to add space at the start and at the end
		bodyString = " " + bodyString + " ";

		searchWords = searchWords.split(" ");
		for (var i = 0; i < searchWords.length; i++) {
			var word = searchWords[i].trim();
			if (word.length > 0) {
				var wordVoweledByRegExp = this.processArabicWord(word, true);
				bodyString = bodyString.replace(
					new RegExp(wordVoweledByRegExp, 'g'), //for a regular exp from the string
					function (found) {                    //function to handle the replacement
						//can skip first and last word breakers from highlighting
						var i = 0;
						var result = "";

						//Add all initial boundary characters
						while (wordBoundary.indexOf(found[i]) != -1) { //is a boundary char
							result += found[i];
							i++;
						}
						var spanStart = '<span class="highlight">';
						result += spanStart;
						//Add normal characters up to next boundary
						while (wordBoundary.indexOf(found[i]) == -1 &&
						i < found.length) { //is not a boundary char
							result += found[i];
							i++;
						}
						var spanEnd = '</span>';
						result += spanEnd;
						//Add remaining characters
						result += found.substring(i, found.length);
						return result; // The replaced string
					}
				);
			}
		}
		//Now, remove the inserted space at the start and at the end
		bodyString = bodyString.substring(1, bodyString.length - 1);
		return bodyString;
	};


	this.highlightSubstring = function (bodyString, searchWords) {
		if (searchWords === undefined) {
			return bodyString;
		}
		//Because of word boundary problem, I have to add space at the start and at the end
		//bodyString = " " + bodyString + " ";
		searchWords = searchWords.split(" ");
		for (var i = 0; i < searchWords.length; i++) {
			var word = searchWords[i].trim();
			if (word.length > 0) {
				var wordVoweledByRegExp = this.processArabicWord(word, false);
				bodyString = bodyString.replace(
					new RegExp(wordVoweledByRegExp, 'g'), //for a regular exp from the string
					function (found) {                    //function to handle the replacement
						//&zwj;   zero-width joiner, see, http://stackoverflow.com/questions/11155849/partially-colored-arabic-word-in-html?rq=1
						// and http://www.user.uni-hannover.de/nhtcapri/bidirectional-text.html
						var spanStart = '&zwj;<span class="highlight">';
						var spanEnd = '&zwj;</span>';
						return spanStart + found + spanEnd; // The replaced string
					}
				);
			}
		}
		return bodyString;
	};

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
///MAKE IT RUN THROUGH TEST CASES


	this.highlightStatement = function (bodyString, searchWords) {
		if (searchWords === undefined) {
			return bodyString;
		}
		//Because of word boundary problem, I have to add space at the start and at the end
		//bodyString = " " + bodyString + " ";
		//searchWords = searchWords.split(" ");
		//for (var i = 0; i < searchWords.length; i++) {
		searchWords = searchWords.trim();
		if (searchWords.length > 0) {
			var wordVoweledByRegExp = this.processArabicWord(searchWords, false);
			bodyString = bodyString.replace(
				new RegExp(wordVoweledByRegExp, 'g'), //for a regular exp from the string
				function (found) {                    //function to handle the replacement
					var spanStart = '<span class="highlight">';
					var spanEnd = '</span>';
					return spanStart + found + spanEnd; // The replaced string
				}
			);
		}
		//}
		return bodyString;
	};

};
