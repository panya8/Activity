
function formatDateText(date) 
{
    date = (date instanceof Date) ? date : new Date(date);
    var dd = (date.getDate()).toString().padStart(2, '0');
    var mm = (date.getMonth() + 1).toString().padStart(2, '0'); 
    var yyyy = date.getFullYear().toString();
    return dd + '/' + mm + '/' + yyyy;
}

function formatDateTimeText(date) 
{
    date = (date instanceof Date) ? date : new Date(date);

    var dd = (date.getDate()).toString().padStart(2, '0');
    var mm = (date.getMonth() + 1).toString().padStart(2, '0'); 
    var yyyy = date.getFullYear().toString();
    var hh = (date.getHours()).toString().padStart(2, '0');
    var nn = (date.getMinutes() + 1).toString().padStart(2, '0'); 
    return dd + '/' + mm + '/' + yyyy + ' ' + hh + ':' + nn;
}

function formatTimeText(date) 
{
    date = (date instanceof Date) ? date : new Date(date);
    var hh = (date.getHours()).toString().padStart(2, '0');
    var nn = (date.getMinutes() + 1).toString().padStart(2, '0'); 
    return hh + ':' + nn;
}

if (window) window.exportDataToCSV = function exportDataToCSV(rows, headers, filename) {
    if (!rows) return false;
      
    var csv = '';
    //console.log('exportDataToCSV', headers, rows);
    
    if (headers)  {
        var line = [];
        for(var name in headers ) {
            line.push(headers[name]);
        }
        csv += line.join(',');
        csv += "\n";
    }
        

    for(var r in rows) {
        var row = rows[r];
        var line = [];
        for(var name in headers ) {
            line.push(row[name]);
        }
        csv += line.join(',');
        csv += "\n";
    }; 
  
    console.log(csv);
    
    const anchor = document.createElement('a');
    anchor.href = 'data:text/csv;charset=utf-8,%EF%BB%BF' + encodeURIComponent(csv);
    anchor.target = '_blank';
    anchor.download = filename || 'export.csv';
    anchor.click(); 
}

if (window) window.formatTimeText = formatTimeText;
if (window) window.formatDateText = formatDateText;
if (window) window.formatDateTimeText = formatDateTimeText;

