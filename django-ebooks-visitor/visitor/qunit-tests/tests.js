QUnit.test("Test highlight words", function (assert) {
	assert.equal('Hello <span class=\"highlight\">World</span>', utils.highlight("Hello World", "World"));
});

QUnit.test("Test highlight substring", function (assert) {
	assert.equal(utils.highlightSubstring("Hello World", "ld"),
							'Hello Wor&zwj;<span class=\"highlight\">ld&zwj;</span>');
});

QUnit.test("Test highlight statement", function (assert) {
	assert.equal(utils.highlightStatement("Hello World and Ahmed", "World and"),
							'Hello <span class=\"highlight\">World and</span> Ahmed');
});




//QUnit.test( "Test regular expression replacement", function( assert ) {
//	assert.equal(utils.highlight("Hello World", "Wor"),
//		'Hello <span class=\"highlight\">Wor</span>ld');
//
//});
