let a = []
let l = document.querySelector("#history-app").shadowRoot.querySelector("#history").shadowRoot.querySelectorAll(".no-outline");
l.forEach((i) => a.push(i.shadowRoot.querySelector("#link > history-searched-label").innerHTML))
console.log(a);