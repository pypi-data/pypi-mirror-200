var gadjo_js = gadjo_js || {};
(function () {
    if (gadjo_js.loaded) return;
    gadjo_js.loaded = true;
    var $ = jQuery;
    var popup_script_loaded = {};
    var deferred_timeout = function (duration) {
        var dfd = $.Deferred();
        setTimeout(function () {
            dfd.resolve();
        }, duration);
        return dfd.promise();
    }
    window.displayPopup = function(event)
    {
        /* Opens the target link into a dialog box
         *
         * The target link is extracted from the @href attribute for anchors or
         * from the @data-url attribute for other tags.
         *
         * The dialog title is extracted from "#appbar h2" (this selector can be
         * changed with a @data-title-selector attribute on the anchor tag).
         *
         * The dialog content is extracted from "form" (this selector can be
         * changed with a @data-selector attribute).
         *
         * Buttons (both <button> and <a>) are extracted from the content and
         * converted into proper dialog buttons.  A button with "cancel" as its
         * class will have its action changed to simply close the dialog, without
         * server processing.
         *
         * After loading the dialog content, a gadjo:dialog-loaded event is
         * triggered on the anchor with the dialog content as argument.
         *
         * Alternatively the server may notice the ajax request and answer with
         * an appropriate JSON response. In that case it should have a 'content'
         * attribute with the HTML content, or a 'location' attribute in case of
         * a redirect.
         *
         * In case of such a redirect, a gadjo:dialog-done event is triggered on
         * the anchor and can be cancelled to prevent the default redirect
         * behaviour.
         *
         * The JSON support depends on the presence of the jQuery Form plugin.
         *
         * Submit is done in place if the $anchor has a data-inplace-submit="true"
         * attribute, a gadjo:dialog-done event is triggered on success, a
         * gadjo:dialog-submit-error event is triggered on failure.
         *
         * Set data-autoclose-dialog="true" to close the dialog box after the
         * submit.
         *
         * Dialog is modal by default, set data-modal="false" for non-modal
         * dialogs.
         */
        var $anchor = $(this);
        var url = $anchor.attr('href') || $anchor.data('url');
        var selector = $anchor.data('selector') || 'form:not(.gadjo-popup-ignore)';
        var title_selector = $anchor.data('title-selector') || '#appbar h2';
        var inplace_submit = $anchor.data('inplace-submit');
        var autoclose_dialog = $anchor.data('autoclose-dialog');
        var modal = $anchor.data('modal');
        if (url == '#') {
            return false;
        }
        if (modal === undefined) {
            modal = true;
        }

        function show_error(message) {
          /* Add a div to body to show an error message and fade it out after 3
           * seconds */
          $('<div id="gadjo-ajax-error"></div>')
            .text(message)
            .appendTo('body')
            .delay(3000)
            .fadeOut(400, function () {
              $(this).remove();
            });
        }

        function ajaxform_submit(data, status, xhr, form) {
            if ('location' in data) {
                var e = $.Event('gadjo:dialog-done');
                if (document.body.contains($anchor[0])) {
                    $anchor.trigger(e, data);
                } else {
                    $(document).trigger(e, data);
                }
                /* check if the event action has been prevented, and don't do
                 * anything in that case. */
                if (! e.isDefaultPrevented()) {
                    if (data.location.split('#')[0] == window.location.href.split('#')[0]) {
                        window.location.reload(true);
                    }
                    window.location = data.location;
                }
            } else {
                var $form = $(form);
                $form.empty().append($(data.content).find(selector).children());
                $form.find('.buttons').hide();
                if (document.body.contains($anchor[0])) {
                  $anchor.trigger('gadjo:dialog-loaded', $form);
                } else {
                  $(document).trigger('gadjo:dialog-loaded', $form);
                }
            }
        }

        /* Close existing dialog boxes */
        $(".ui-dialog-content").dialog("destroy");

        $.ajax({
            url: url,
            success: function(html) {
                var is_json = typeof html != 'string';
                if (is_json) {
                    /* get html out of json */
                    var html = html.content;
                } else {
                    var html = html;
                }
                var $html = $(html);
                /* load additional scripts from popup */
                var $script = $html.filter('script[src]');
                var loading = [];
                for (var i = 0; i < $script.length; i++) {
                    var script = $script[i];
                    var src = script.attributes.src.value;
                    if ($('script[src="' + src + '"]').length) {
                        continue;
                    }
                    if (popup_script_loaded[src]) {
                        continue;
                    }
                    popup_script_loaded[src] = true;
                    loading.push($.ajax({
                        url: src,
                        dataType: 'script',
                        cache: true,
                        success: function () {},
                    }));
                }
                /* load additional stylesheets from popup */
                var $stylesheet = $html.filter('link[rel="stylesheet"]');
                for (var i = 0; i < $stylesheet.length; i++) {
                    var stylesheet = $stylesheet[i];
                    var href = stylesheet.attributes.href.value;
                    if ($('link[rel="stylesheet"][href="' + href + '"]').length) {
                        continue;
                    }
                    $(stylesheet).appendTo($('head'));
                }
                /* add millisecond timeout to let additional scripts load */
                $.when(loading, deferred_timeout(100)).always(function () {
                    /* get content and form (if different) ouf of html */
                    var $content = $html.find(selector);
                    if ($content.is('form')) {
                        var $form = $content;
                    } else {
                        var $form = $content.find('form');
                    }

                    /* get title out of html */
                    var title = $html.find(title_selector).text();

                    $content.dialog({
                      modal: modal,
                      'title': title,
                      width: 'auto',
                      close: function (ev, ui) {
                        $(this).dialog('destroy');
                      },
                    });

                    /* if the form doesn't have an @action attribute, set it to URL */
                    if (! $form.attr('action')) {
                        $form.attr('action', url);
                    }

                    /* hide buttons from content and convert buttons (<button> and <a>)
                     * into proper dialog buttons */
                    $content.find('.buttons').hide();

                    var buttons = Array();
                    $content.find('.buttons button, .buttons a').each(function(idx, elem) {
                        var $elem = $(elem);
                        var button = Object();

                        button.text = $elem.text();
                        if ($elem.prop('disabled')) {
                            button.disabled = 'disabled';
                        }
                        if ($elem.hasClass('cancel')) {
                            /* special behaviour for the cancel button: do not send
                             * anything to server, just close the dialog */
                            button.click = function() { $content.dialog('destroy'); return false; };
                        } else {
                            button.click = function() {
                                if (inplace_submit) {
                                    var action_url = $form.attr('action');
                                    if ($form[0].checkValidity() === false) {
                                        /* if HTML5 validation fails, we trigger a
                                         * click to get the errors displayed */
                                        $form.find('button').click();
                                        return false;
                                    }
                                    $('.ui-dialog-buttonpane button').button('disable');
                                    $.ajax({
                                        type: 'POST',
                                        url: action_url,
                                        data: $form.serialize(),
                                    }).success(function(data) {
                                        $anchor.trigger('gadjo:dialog-done', data);
                                        $content.dialog('destroy');
                                    }).fail(function() { $anchor.trigger('gadjo:dialog-submit-error');
                                    });
                                } else {
                                    if ($elem.is('a')) {
                                        window.location = $elem.attr('href');
                                    } else {
                                        $elem.click();
                                    }
                                    var validated = true;
                                    $form.find('input, textarea').each(function() {
                                        if ($(this)[0].checkValidity != undefined) {
                                            validated &= $(this)[0].checkValidity();
                                        }
                                    })
                                    if (autoclose_dialog & validated) {
                                        $content.dialog('destroy');
                                    }
                                }
                                return false;
                            };
                        }

                        /* add custom classes to some buttons */
                        if ($elem.hasClass('submit-button')) {
                            button.class = 'submit-button';
                        } else if ($elem.hasClass('cancel') || $elem.hasClass('cancel-button')) {
                            button.class = 'cancel-button';
                        } else if ($elem.hasClass('delete-button')) {
                            button.class = 'delete-button';
                        }
                        buttons.push(button);
                    });

                    buttons.reverse();
                    $content.dialog('option', 'buttons', buttons);

                    /* focus initial input field */
                    var $form_fields = $form.find('input:visible, textarea:visible, select:visible');
                    if ($form_fields.length) {
                        $form_fields[0].focus();
                    }

                    /* if received content was in json, apply jQuery Form plugin on it */
                    if (is_json && $.fn.ajaxForm != undefined) {
                        $form.ajaxForm({
                          success: ajaxform_submit,
                          error: function (jqXHR, textStatus, errorThrown) {
                            show_error("Dialog box submit failed: " + textStatus + " " + errorThrown);
                          }
                        });
                    }
                    $anchor.trigger('gadjo:dialog-loaded', $content);
                });
                return false;
            },
            error: function (jqXHR, textStatus, errorThrown) {
              show_error("Dialog box loading failed: " + textStatus + " " + errorThrown);
            }
        });
        return false;
    }

    // Tabs
    // adapted from https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Tab_Role
    gadjo_js.Tabs = function(tabs_el) {
      this.parent = tabs_el;
      this.tabList = this.parent.querySelector('[role="tablist"]');
      this.tabs = this.tabList.querySelectorAll('[role="tab"]');
      this.tabpanels = this.parent.querySelectorAll('[role="tabpanel"]');

      this.init();
    }

    gadjo_js.Tabs.prototype = {
      init : function() {
        const _self = this;

        // Add a click event handler to each tab
        this.tabs.forEach(function(tab) {
          tab.addEventListener('click', function(e) {_self.selectTab.call(_self, e)});
        });

        // Enable arrow navigation between tabs in the tab list
        let tabFocus = 0;

        this.tabList.addEventListener('keydown', function(e) {
          // Move up & down
          if (e.key === "ArrowDown" || e.key === "ArrowUp") {
            e.preventDefault();
            _self.tabs[tabFocus].setAttribute('tabindex', -1);
            if (e.key === "ArrowDown") {
              tabFocus++;
              // If we're at the end, go to the start
              if (tabFocus >= _self.tabs.length) {
                tabFocus = 0;
              }
            } else if (e.key === "ArrowUp") {
              tabFocus--;
              // If we're at the start, move to the end
              if (tabFocus < 0) {
                tabFocus = _self.tabs.length - 1;
              }
            }

            _self.tabs[tabFocus].setAttribute('tabindex', 0);
            _self.tabs[tabFocus].focus();
          }
        });
      },

      selectTab: function(e) {
        const btn = e.target && e.target || e;

        // Remove all current selected tabs
        this.tabList
          .querySelectorAll('[aria-selected="true"]')
          .forEach(function(t) { t.setAttribute('aria-selected', false); });

        // Set this tab as selected
        btn.setAttribute('aria-selected', true);

        // Hide all tab panels
        this.tabpanels.forEach(function(p) { p.hidden = true });

        // Show the selected panel
        this.parent
          .querySelector('#' + btn.getAttribute('aria-controls'))
          .hidden = false;

        // Adjust URL to mention selected tab
        const url = new URL(document.location);
        const prefix = btn.getAttribute('aria-controls').split('-')[0];
        url.hash = '#open:' + btn.getAttribute('aria-controls').substring(prefix.length + 1);
        history.replaceState(null, '', url);

        // Trigger gadjo:tab-selected event on panel
        $(this.parent.querySelector('#' + btn.getAttribute('aria-controls'))).trigger('gadjo:tab-selected');
        return false;
      }
    }

    window.addEventListener('DOMContentLoaded', function() {
      $(document.querySelectorAll('.pk-tabs')).each(function(i, el) {
        el.tabs = new gadjo_js.Tabs(el);
      });

      /* focus tab from #open:<tab slug> anchor, to point to open panel */
      if (document.location.hash && document.location.hash.indexOf('#open:') == 0) {
        const $tab_button = $('#tab-' + document.location.hash.substring(6) + '[role=tab]');
        if ($tab_button.length) {
          $tab_button.parents('.pk-tabs')[0].tabs.selectTab($tab_button[0]);
        }
      }
    });

    var storage = undefined;
    try {
        window.localStorage._gadgo_test = true;
        window.localStorage.removeItem('_gadjo_test');
        storage = window.localStorage;
    } catch(e) {
        try {
            window.sessionStorage._gadjo_test = true;
            window.sessionStorage.removeItem('_gadjo_test');
            storage = window.sessionStorage;
        } catch(e) {
            storage = Object();
        }
    }

    var cookie_domain = window.location.hostname.split('.').slice(1).join('.');

    function readCookie(name) { /* http://www.quirksmode.org/js/cookies.html */
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
    }

    function set_sidepage_status(sidepage_status) {
      storage.sidepage_status = sidepage_status;
      if (cookie_domain) {
        var date = new Date();
        date.setTime(date.getTime() + (10 * 86400 * 1000)); /* a long week */
        document.cookie = 'gadjo_sidepage_status=' + sidepage_status +
                          '; expires=' + date.toGMTString() +
                          (window.location.protocol == "https:" && "; Secure" || "") +
                          '; sameSite=Strict' +
                          '; domain=.' + cookie_domain +
                          '; path=/';
      }
    }
    function get_sidepage_status() {
      if (window.location.protocol == 'file:') {
        /* don't open sidepage when loading from a file:// */
        return 'collapsed';
      }
      var sidepage_status = null;
      if (cookie_domain) {
        sidepage_status = readCookie('gadjo_sidepage_status');
      } else {
        sidepage_status = storage.sidepage_status;
      }
      if (!sidepage_status &&
              typeof(GADJO_DEFAULT_SIDEPAGE_STATUS) !== "undefined") {
        return GADJO_DEFAULT_SIDEPAGE_STATUS;
      }
      return sidepage_status;
    }
    document.addEventListener('DOMContentLoaded', function() {
      if (document.body.dataset.gadjo === 'true' && document.getElementById('sidepage')) {
        document.body.setAttribute('data-has-sidepage', 'true');
        if (storage.gadjo_sidebar_menu) {
          $('#sidepage-menu').empty().append($(storage.gadjo_sidebar_menu));
        }
        if (window.innerWidth > 760 && get_sidepage_status() == 'expanded') {
          document.body.className += ' sidepage-expanded';
        }
      }
    });

    $(function() {
      $(document).on('click.gadjo', 'a[rel=popup], a[data-popup]', displayPopup);
      if ($('#sidepage').length) {
        var sidepage_button = $('#sidepage #applabel');
        sidepage_button.on('click', function() {
          $('body').addClass('enable-transitions');
          $('body').toggleClass('sidepage-expanded');
          if ($('body').hasClass('sidepage-expanded')) {
             set_sidepage_status('expanded');
          } else {
             set_sidepage_status('collasped');
          }
          setTimeout(function() {
            // delay to get the CSS transition to run
            $(window).trigger('gadjo:sidepage-toggled');
          }, 500);
        });
      }
    });
    $(function () { /* foldable elements with memory */
      function gadjo_unfold_saved() {
        $('.gadjo-folded').each(function (idx, elem) {
          if (elem.id && sessionStorage['gadjo-foldable-id-' + elem.id + '-' + window.location.pathname] == "true") {
              $(elem).removeClass('gadjo-folded');
          }
        });
      }
      gadjo_unfold_saved()
      $(document).on('gadjo:content-update', gadjo_unfold_saved);
      $('body').on('click', '.gadjo-foldable-widget', function (event) {
        var $parent = $(event.target).closest('.gadjo-foldable');
        $parent.toggleClass('gadjo-folded');
        if ($parent[0].id) {
            sessionStorage['gadjo-foldable-id-' + $parent[0].id + '-' + window.location.pathname] = ! $parent.is('.gadjo-folded');
        }
      });
    });
    $(function () { /* foldable sections */
      $('.section.foldable > h2, .section.foldable > h3').on('click', function() {
        $(this).parent().toggleClass('folded');
      });
    });
    $(function () {
      if ($('body').data('gadjo')) {
        /* add × to close notification messages */
        $('.messages > li').each(function(idx, elem) {
          var elem = $('<a aria-hidden="true" class="close">×</a>');
          $(elem).on('click', function() {
            $(this).parent('li').fadeOut('slow');
          });
          $(this).prepend(elem);
        });
      }
    });
    $(function() {
      $(document.querySelectorAll('.extra-actions-menu')).each(function(i, el) {
        this.setAttribute('id', 'extra-actions-menu');
      });
      $(document.querySelectorAll('.extra-actions-menu-opener')).each(function(i, el) {
        this.setAttribute('tabindex', 0);
        this.setAttribute('aria-label', 'Menu');  // XXX: translation
        this.setAttribute('aria-controls', 'extra-actions-menu');
        this.setAttribute('aria-expanded', 'false');
        this.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            $(this).toggleClass('open');
            $('.extra-actions-menu').toggleClass('open');
            this.setAttribute('aria-expanded', $(this).is('.open'));
            e.preventDefault();
          }
        });
        this.addEventListener('click', function() {
          $(this).toggleClass('open');
          $('.extra-actions-menu').toggleClass('open');
          this.setAttribute('aria-expanded', $(this).is('.open'));
        });
      });
    });
    $(function() {
      $(document).on('click auxclick', '.clickable-rows tr', function(event) {
        var $target = $(event.target);
        if ($target.is('input, button, a')) {
          return true;
        }
        if (window.getSelection().toString()) {
          return false;
        }
        var href = $(this).data('url') || $(this).find('a[href]').prop('href');
        if (href) {
          if (event.which == 2 || event.ctrlKey) {
            window.open(href, '_blank');
          } else {
            window.location = href;
          }
          return false;
        }
      });
    });
    $(function() {
      $('.varname').on('click', function() {
        var doc = window.document, sel, range;
        if (window.getSelection && doc.createRange) {
          sel = window.getSelection();
          range = doc.createRange();
          range.selectNodeContents(this);
          sel.removeAllRanges();
          sel.addRange(range);
        } else if (doc.body.createTextRange) {
          range = doc.body.createTextRange();
          range.moveToElementText(this);
          range.select();
        }
        return false;
      });
    });
    $(document).on('publik:menu-loaded', function() {
      storage.gadjo_sidebar_menu = document.getElementById('sidepage-menu').innerHTML;
    });
})();
