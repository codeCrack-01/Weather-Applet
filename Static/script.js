$(document).ready(function(){
    $('#openModalBtn').click(function(){
        $('#searchBox').modal('show');
    });
    var text = $('#camelCase').text()
    var newText = toPascalCaseWithSpaces(text)

    $('#camelCase').text(newText)
});

function toPascalCaseWithSpaces(str) {
    // Convert string to camel case
    let pascalCaseStr = str.replace(/(?:^\w|[A-Z]|\b\w|\s+)/g, function(match, index) {
      if (+match === 0) return ""; // or if (/\s+/.test(match)) for white spaces
      return index === 0 ? match.toLowerCase() : match.toUpperCase();
    });
    
    // Remove spaces and capitalize each word
    pascalCaseStr = pascalCaseStr.replace(/(?:^\w|[A-Z]|\b\w|\s+)/g, function(match) {
      return match.toUpperCase();
    }).replace(/\s+/g, '');

    // Add spaces between pascal case words
    pascalCaseStr = pascalCaseStr.replace(/([a-z])([A-Z])/g, '$1 $2');

    return pascalCaseStr;
}