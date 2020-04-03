// namespace
window.semantic = {
  handler: {}
};
const
  $menu = $('#toc');
// ready event
semantic.ready = function () {
  // main sidebar
  $menu
    .sidebar({
      dimPage: true,
      transition: 'overlay',
      mobileTransition: 'uncover'
    })
  ;
  // launch buttons
  $menu
    .sidebar('attach events', '.launch.button, .view-ui, .launch.item')
  ;
};
// attach ready event
$(document)
  .ready(semantic.ready)
;
