chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
  }
  if (changeInfo.status === 'complete') {
    console.log(tab.url);
    if(tab.url.startsWith("https://www.google.com/search")){
      search_word = tab.title.substr(0,(tab.title.length-12));
      console.log(search_word);
    }else{
      console.log(tab.title);
    }
  }
});