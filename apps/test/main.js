const rand = Math.random().toString(36).slice(2, 7);
localStorage.setItem(rand, rand);

console.log(location.href);
console.log(localStorage);

window._external.print_goodness();
