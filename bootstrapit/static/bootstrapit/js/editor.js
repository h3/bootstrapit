(function($){

    $(window).bind('resize.bootstrapit', function(e) {
        var h = $(window).height() - 110;
        $('.CodeMirror').height(h)
            .find('.CodeMirror-scroll').height(h); // Weird ..
    });

    $('.viewport-save').live('click.bootstrapit', function(){
        var vp = $(this).parents('.viewport').data('file');
        $.bootstrapit.saveViewport(vp);
    });

    $('.viewport-close').live('click.bootstrapit', function(){
        $(this).parents('.viewport').remove();
    });

    $('.cm-number')
        .live('mouseover', function() {
            $(this).addClass('hover');
            if ($(this).text()[0] == '#') {
                $(this).css('border-right', '20px solid '+$(this).text());
            }
        })
        .live('mouseleave', function() {
            $(this).removeClass('hover');
            $(this).css('border-right', 0);
        });

    $.bootstrapit = (function() {

        this.preview = window.parent;
        this.viewports = {};

        this.createEditor = function(element) {
            return CodeMirror(element.get(0), {
                dynamic: true
            });
        };

        this.createViewport = function(filename, title) {
            $('.viewport').hide();
            var editor,
                lesspath = $('body').data('less-path'),
                viewport = $([
                '<div class="viewport" data-file="', filename,'">',
                    '<div class="viewport-toolbar pull-right">',
                        '<div class="btn-group">',
                            '<button data-toggle="dropdown" class="btn dropdown-toggle">Buffers <span class="caret"></span></button>',
                            '<ul id="open-buffers" class="dropdown-menu">',
                                '<li><a href="#">Save all</a></li>',
                                '<li><a href="#">Save and close all</a></li>',
                                '<li class="divider"></li>',
                                '<li><a href="#variables.less">variables.less</a></li>',
                                '<li><a href="#layout.less">layout.less</a></li>',
                            '</ul>',
                            '<button class="btn viewport-save" data-loading-text="Saving...">Save</button>',
                            '<button class="btn viewport-close">Close</button>',
                        '</div>',
                    '</div>',
                    '<h1>',
                        '<span class="viewport-title">', title, ' </span>',
                        '<small class="viewport-filename">', filename, '</small>',
                    '</h1>',
                    '<div class="viewport-content" />',
                '</div>'].join('')).appendTo('#bootstrapit-editor');

            editor = this.createEditor(
                        viewport.find('.viewport-content'));

            $(window).trigger('resize.bootstrapit');
            this.loadFile(lesspath + filename, editor);

            this.viewports[filename] = {
                title: title,
                filename: filename,
                viewport: viewport,
                editor: editor
            };

            return this.viewports[filename];
        };

        this.showViewport = function(filename) {
            $('.viewport').hide();
            return this.viewports[filename].viewport.show();
        };

        this.getViewport = function(filename) {
            return this.viewports[filename];
        };

        this.saveViewport = function(filename) {
            var vp = $.bootstrapit.getViewport(filename);
            $.post('/api/editor', {
                    filename: filename,
                    content: vp.editor.getValue(),
                }, function(){
                    console.log('Saved..');
                });
        };

        this.loadFile = function(path, editor) {
            $.get(path, function(rs, statusCode) {
                if (statusCode == 'success') {
                    editor.setValue(rs);
                    $(editor.getWrapperElement()).find('.cm-number')
                        .each(function(i, el){
                            var t = $(el).text()
                            if (t.slice(0,1) == '#' && (t.length == 4 || t.length == 7)) {
                                $(el).data('color', t).colorpicker().on('changeColor', function(ev){
                                    $(this).text(ev.color.toHex());
                                });
                            }
                        })
                }
            });
        };

        return this;
    })();

    $(function(){
        $('.bootstrapit-file').bind('click.bootstrapit', function(e){
            var a = $(this),
                filename = a.attr('href').replace('#', '');
            if (a.data('editor-viewport')) {
                $.bootstrapit.showViewport(filename);
            }
            else {
                a.data('editor-viewport', 
                    $.bootstrapit.createViewport(filename, a.text()));
            }
        });
    });
})(jQuery);

