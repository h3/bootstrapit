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
        var vp = $(this).parents('.viewport').data('file');
        $.bootstrapit.closeViewport(vp);
        $('.viewport:first').show();
    });

    $('.bootstrapit-file').live('click', function(e){
        var a = $(this),
            filename = a.attr('href').replace('#', '');
        if (typeof($.bootstrapit.viewports[filename]) != 'undefined') {
            $.bootstrapit.showViewport(filename);
        }
        else {
            $.bootstrapit.createViewport(filename, a.text());
        }
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

        this.updateBufferLists = function() {
            $('.open-buffers-list .bootstrapit-file').parent().remove();
            $.each(this.viewports, function(filename, vp){
                $('<li><a href="#'+ filename +'" class="bootstrapit-file">'+ filename +'</a></li>')
                    .appendTo('.open-buffers-list');
            });
        },

        this.createViewport = function(filename, title) {
            $('.viewport').hide();
            var editor,
                lesspath = $('body').data('less-path'),
                viewport = $([
                '<div class="viewport" data-file="', filename,'">',
                    '<div class="viewport-toolbar pull-right">',
                        '<div class="btn-group">',
                            '<button data-toggle="dropdown" class="btn dropdown-toggle">Buffers <span class="caret"></span></button>',
                            '<ul class="dropdown-menu open-buffers-list">',
                                '<li><a href="#">Save all</a></li>',
                                '<li><a href="#">Save and close all</a></li>',
                                '<li class="divider"></li>',
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
            this.updateBufferLists();
            return this.viewports[filename];
        };

        this.showViewport = function(filename) {
            $('.viewport').hide();
            return $.bootstrapit.getViewport(filename).viewport.show();
        };

        this.getViewport = function(filename) {
            return this.viewports[filename];
        };

        this.closeViewport = function(filename) {
            this.viewports[filename].viewport.remove();
            delete this.viewports[filename];
            this.updateBufferLists();
        };

        this.getVersionChoice = function(choices){
            console.log('get version choice ' + choices);
            return true;
        };

        this.getThemeChoice = function(choices){
            console.log('get theme choice ' + choices);
            return true;
        };

        this.getLessFileChoice = function(choices){
            console.log('get .less file choice ' + choices);
            return true;
        };

        this.saveViewport = function(filename) {
            var vp = $.bootstrapit.getViewport(filename);
            $.post('/api/editor/', {
                    filename: filename,
                    content: vp.editor.getValue(),
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                }, function(json){
                    console.log(json);
                    if (json['status'] != 'ok'){
                        if (json['status'] == 'BV' || json['status'] == 'BV-404'){
                            getVersionChoice(json['choices']);
                        }else if (json['status'] == 'theme' || json['status'] == 'theme-404'){
                            getThemeChoice(json['choices']);
                        }else if(json['status'] == 'file'){
                            getLessFileChoice(json['choices']);
                        }else{
                            console.log('erreur inconnue');
                        }
                    }else{
                    console.log('Saved..');
                    }
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
})(jQuery);

