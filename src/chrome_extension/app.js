const url = 'http://localhost:8000';
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
  }
  if (changeInfo.status === 'complete') {
    if(tab.url.startsWith("https://www.google.com/search")){
      search_word = tab.title.substr(0,(tab.title.length-12));
      console.log(search_word);//
      data = {query : search_word}
      fetch(url+"/on_google_search", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(data)
      })
      .then((response) => response.json())
      .then((check) => console.log(check));
    }else{
      console.log(tab.title);//
      data = {content : tab.title}
      fetch(url+"/on_page_open", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(data)
      })
      .then((response) => response.json())
      .then((check) => console.log(check));
    }
  }
});