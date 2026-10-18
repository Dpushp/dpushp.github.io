const filters = document.querySelector('.filters');
const buttons = [...document.querySelectorAll('[data-filter]')];
const papers = [...document.querySelectorAll('[data-topic]')];
filters.hidden = false;
buttons.forEach(button => button.addEventListener('click', () => {
  buttons.forEach(item => {
    const selected = item === button;
    item.classList.toggle('active', selected);
    item.setAttribute('aria-pressed', String(selected));
  });
  papers.forEach(paper => {
    paper.hidden = button.dataset.filter !== 'all' && paper.dataset.topic !== button.dataset.filter;
  });
}));
