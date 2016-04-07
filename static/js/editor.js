$(document).ready(function() {
	var simplemde = new SimpleMDE({ 
		element: $("#field-content")[0],
		spellChecker: false,
		toolbar: ["bold", "italic", "heading", "|", "code", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "preview", "fullscreen"]
	});
});