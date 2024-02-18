
function initializePreviousData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const previousData = data;

  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty('previousData', JSON.stringify(previousData));
}

function printChangedRowAndNewRow() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const scriptProperties = PropertiesService.getScriptProperties();
  const previousData = JSON.parse(scriptProperties.getProperty('previousData'));

  for (let i = 1; i < data.length; i++) {
    if (i >= previousData.length) {
      Logger.log('New row added:' + data[i]);
      resp = sendDataToAPI(i, data[i])
      sheet.getRange(i+1, 10).setValue(resp["status"]);
      sheet.getRange(i+1, 11).setValue(resp.message);
      sheet.getRange(i+1, 12).setValue(resp.updated_at);
    } else {
      let rowChanged = false;
      for (let j = 0; j < 9; j++) {
        if (data[i][j] !== previousData[i][j]) {
          rowChanged = true;
          break;
        }
      }
      if (rowChanged) {
        Logger.log('Row ' + (i + 1) + ' changed:'+ data[i]);
        resp = sendDataToAPI(i, data[i])
        sheet.getRange(i+1, 10).setValue(resp.status);
        sheet.getRange(i+1, 11).setValue(resp.message);
        sheet.getRange(i+1, 12).setValue(resp.updated_at);
      }
    }
  }
  scriptProperties.setProperty('previousData', JSON.stringify(data));
}

function onSheetEdit(e) {
  printChangedRowAndNewRow();
}
function setup() {
  initializePreviousData();
}

function sendDataToAPI(id, data) {
  var input = {
      "id": id,
      "news_title": String(data[0]),
      "news_detail": String(data[1]),
      "news_image": String(data[2]),
      "quiz_title": String(data[3]),
      "quiz_type": String(data[4]),
      "quiz_choice": String(data[5]),
      "quiz_detail": String(data[6]),
      "quiz_description": String(data[7]),
      "quiz_answer": String(data[8]),
    };
  var apiUrl = 'https://test.accx.dev/news/update';
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(input)
  };
  var response = UrlFetchApp.fetch(apiUrl, options);
  return JSON.parse(response.getContentText())
}