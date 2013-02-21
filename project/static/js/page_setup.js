$(function() {
  // If we're not using the sidebar, expand the main content
  if ($("#no-sidebar").length > 0) {
    $("#content").toggleClass('span9');
  }

  // If we're not using the breadcrumb, add 20px of margin to the body
  // to keep spacing the same from page to page
  if ($("#no-breadcrumb").length > 0) {
    $("#content").parent().css('margin-top', '20px');
  }

  // If the URL starts with "/weblog/", gray out the blog tab
  if (window.location.pathname.match(/^\/weblog\//) != null) {
    $("#zinnia-tab").toggleClass("active");
  }

  // If the URL starts with "/profile/", gray out the profile tab
  if (window.location.pathname.match(/^\/profile/) != null) {
    $("#profile-tab").toggleClass("active");
  }
});
