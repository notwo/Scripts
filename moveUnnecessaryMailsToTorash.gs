function deleteSocialThreads() {
  var targetThreads = GmailApp.search("category:social", 0, 500);
  for (var i = 0;i < targetThreads.length;i++) {
    targetThreads[i].moveToTrash();
  }
}
function deletePromotionsThreads() {
  var targetThreads = GmailApp.search("category:promotions", 0, 500);
  for (var i = 0;i < targetThreads.length;i++) {
    targetThreads[i].moveToTrash();
  }
}

/* label_for_searchの中身を変えて実行すれば、狙った中身を全て削除できる */
function deleteTargetThreads() {
  var deleteBorder = 1;
  var label_for_search = 'Shopping/メルカリ';
  var labelSearched = GmailApp.getUserLabelByName(label_for_search);
  if (labelSearched === null || labelSearched === undefined) {
    Logger.log('---- no threads... ----');
    return;
  }
  var targetThreads = GmailApp.search('label:' + label_for_search, 0, 500);
  for (var i = 0;i < targetThreads.length;i++) {
    var messages = targetThreads[i].getMessages();
    var lastMessage = messages[messages.length - 1];
    var lastMessageTime = lastMessage.getDate().getTime();
    var day = parseInt(lastMessageTime / (1000 * 60 * 24));

    if (parseInt(new Date().getTime() / (1000 * 60 * 24)) - day > deleteBorder) {
      targetThreads[i].moveToTrash();
    }
  }
}
