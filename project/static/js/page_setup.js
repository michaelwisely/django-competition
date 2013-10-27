$(function() {
    // If we're not using the sidebar, expand the main content
    if ($("#no-sidebar").length > 0) {
        $("#content").toggleClass('col-md-9');
    }

    // If we're not using the breadcrumb, add 20px of margin to the body
    // to keep spacing the same from page to page
    if ($("#no-breadcrumb").length > 0) {
        $("#content").parent().css('margin-top', '20px');
    }

    // If the URL starts with "/weblog/" or "/about", gray out the
    // siggame tab
    if (window.location.pathname.match(/^\/weblog\//) != null ||
        window.location.pathname.match(/^\/about/) != null) {
        $("#siggame-tab").toggleClass("active");
    }

    // If the URL starts with "/profile/", gray out the profile tab
    if (window.location.pathname.match(/^\/profile/) != null) {
        $("#profile-tab").toggleClass("active");
    }

    // If the URL starts with "/competition"...
    if (window.location.pathname.match(/^\/competition/) != null) {
        $("#competition-tab").toggleClass("active");

        var competition_nav = $("#competition-nav > li");
        var code_nav = $("#code-nav > li");
        var team_nav = $("#team-nav > li");
        var registration_nav = $("#registration-nav > li");

        if (window.location.pathname.match(/^\/competition\/[\w\-]+\/$/)) {
            // Activate Competition Details nav button
            $(competition_nav[0]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/games\/$/)) {
            // Activate Games nav button
            $(competition_nav[1]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/submissions\/$/)) {
            // Activate Code Submissions nav button
            $(code_nav[0]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/update-password\/$/)) {
            // Activate Update Repository Password nav button
            $(code_nav[2]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/teams\/$/)) {
            // Activate All Teams nav button
            $(team_nav[0]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/freeagents\/$/)) {
            // Activate Free Agents nav button
            $(team_nav[1]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/team-leave\/$/)) {
            // Activate Team Leave nav button
            $(team_nav[3]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/unregister\/$/)) {
            // Activate Unregister nav button
            $(registration_nav[0]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/team-create\/$/)) {
            // Activate Create Team nav button
            $(team_nav[2]).toggleClass("active");
        } else if (window.location.pathname.match(/^\/competition\/[\w\-]+\/create-repo\/$/)) {
            // Activate Create Repo nav button
            $(code_nav[0]).toggleClass("active");
        }
    }

    if (window.location.pathname.match(/^\/repo/) != null) {
        $("#competition-tab").toggleClass("active");
        $($("#code-nav > li")[1]).toggleClass("active");
    }


    $('#your-competitions').tooltip({placement: "left", delay: 1000});

    // If the URL starts with "/invitation", gray out the profile tab
    if (window.location.pathname.match(/^\/invitation/) != null) {
        $("#invitation-tab").toggleClass("active");
    }

    // If the URL starts with "/docs" gray out the documentation tab
    if (window.location.pathname.match(/^\/docs/) != null) {
        $("#documentation-tab").toggleClass("active");
    }

    // If the URL starts with "/accounts/email", gray out the profile tab
    if (window.location.pathname.match(/^\/accounts\/email/) != null) {
        $("#profile-tab").toggleClass("active");
    }

    // If the URL starts with "/social/connections", gray out the profile tab
    if (window.location.pathname.match(/^\/accounts\/social\//) != null) {
        $("#profile-tab").toggleClass("active");
    }

    // If the URL starts with "/accounts/password", gray out the profile tab
    if (window.location.pathname.match(/^\/accounts\/password\/(change|set)/) != null) {
        $("#profile-tab").toggleClass("active");
    }
});