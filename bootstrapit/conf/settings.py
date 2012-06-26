from django.conf import settings

"""
 Instead of using a model to store different bootstrap versions we will use
 a configuration since we already need to setup file mapping by hand for each versions.

 Workflow
 --------

 - Edit the `BOOTSTRAPIT_BOOTSTRAP_VERSIONS` settings to add/modify bootstrap versions
 - Edit the `BOOTSTRAPIT_BOOTSTRAP_NAV` to specify the file mapping for each bootstrap versions
 - Run this management command to download and cache all bootstrap versions:
   $ django bootstrapit_sync
 - Bootstrapit will go through each specified bootstrap versions and download them if they aren't already present

"""



MEDIA_URL  = getattr(settings, 'BOOTSTRAPIT_MEDIA_URL', settings.MEDIA_URL)
MEDIA_ROOT = getattr(settings, 'BOOTSTRAPIT_MEDIA_ROOT', settings.MEDIA_ROOT)

BOOTSTRAPIT_BOOTSTRAP_VERSIONS = {
    '2.0.4': 'https://github.com/twitter/bootstrap/tarball/v2.0.4',        
    'dev': 'git://github.com/twitter/bootstrap.git',        
}

BOOTSTRAPIT_BOOTSTRAP_NAV = {}


BOOTSTRAPIT_BOOTSTRAP_NAV['2.0.4'] = [
    {'label': u'General',
     'items': [
         {'type': 'file', 'src': 'less/variables.less',   'label': u'Variables'},
         {'type': 'file', 'src': 'less/mixins.less',      'label': u'Mixins'},
         {'type': 'file', 'src': 'less/reset.less',       'label': u'Reset'},
         {'type': 'file', 'src': 'less/sprites.less',     'label': u'Sprites'},
         {'type': 'file', 'src': 'less/utilities.less',   'label': u'Utilities'},
         {'type': 'file', 'src': 'less/close.less',       'label': u'Close icons'},
     ],
    },
    {'label': u'Base CSS',
     'items': [
         {'type': 'file', 'src': 'less/variables.less',   'label': u'Variables'},
         {'type': 'file', 'src': 'less/type.less',        'label': u'Typography'},
         {'type': 'file', 'src': 'less/code.less',        'label': u'Code'},
         {'type': 'file', 'src': 'less/tables.less',      'label': u'Tables'},
         {'type': 'file', 'src': 'less/forms.less',       'label': u'Forms'},
     ],
    },
    {'label': u'Scaffolding',
     'items': [
         {'type': 'file', 'src': 'less/scaffolding.less', 'label': u'Global styles'},
         {'type': 'file', 'src': 'less/grid.less',        'label': u'Grid system'},
         {'type': 'file', 'src': 'less/layouts.less',     'label': u'Layouts'},
         {'type': 'divider'},
         {'type': 'header', 'label': u'Responsive design'},
         {'type': 'file', 'src': 'less/responsive-767px-max.less',    'label': u'767px max'},
         {'type': 'file', 'src': 'less/responsive-768px-979px.less',  'label': u'768px - 979px'},
         {'type': 'file', 'src': 'less/responsive-1200px-min.less',   'label': u'1200px min'},
         {'type': 'file', 'src': 'less/responsive-navbar.less',       'label': u'Navbar'},
         {'type': 'file', 'src': 'less/responsive-utilities.less',    'label': u'Utilities'},
     ],
    },
    {'label': u'Components',
     'items': [
         {'type': 'file', 'src': 'less/scaffolding.less',     'label': u'Global styles'},
         {'type': 'file', 'src': 'less/buttons.less',         'label': u'Buttons'},
         {'type': 'file', 'src': 'less/buttons-groups.less',  'label': u'Buttons groups'},
         {'type': 'file', 'src': 'less/dropdowns.less',       'label': u'Dropdowns'},
         {'type': 'file', 'src': 'less/labels-badges.less',   'label': u'Labels & Badges'},
         {'type': 'file', 'src': 'less/thumbnails.less',      'label': u'Thumbnails'},
         {'type': 'file', 'src': 'less/alerts.less',          'label': u'Alerts'},
         {'type': 'file', 'src': 'less/progress-bars.less',   'label': u'Progress bars'},
         {'type': 'divider'},
         {'type': 'header', 'label': u'Menus'},
         {'type': 'file', 'src': 'less/navs.less',        'label': u'Navigations'},
         {'type': 'file', 'src': 'less/navbar.less',      'label': u'Navbar'},
         {'type': 'file', 'src': 'less/pager.less',       'label': u'Pager'},
         {'type': 'file', 'src': 'less/breadcrumbs.less', 'label': u'Breadcrumbs'},
         {'type': 'divider'},
         {'type': 'header', 'label': u'Miscellaneous'},
         {'type': 'file', 'src': 'less/hero-unit.less',   'label': u'Hero unit'},
         {'type': 'file', 'src': 'less/wells.less',       'label': u'Wells'},
     ],
    },
    {'label': u'Plugins',
     'items': [
         {'type': 'file', 'src': 'less/modals.less',      'label': u'Modal'},
         {'type': 'file', 'src': 'less/dropdowns.less',   'label': u'Dropdown'},
         {'type': 'file', 'src': 'less/tooltip.less',     'label': u'Tooltip'},
         {'type': 'file', 'src': 'less/popovers.less',    'label': u'Popover'},
         {'type': 'file', 'src': 'less/carousel.less',    'label': u'Carousel'},
     ],
    },
]
BOOTSTRAPIT_BOOTSTRAP_NAV['dev'] = BOOTSTRAPIT_BOOTSTRAP_NAV['2.0.4']

BOOTSTRAPIT_EDITOR_DEFAULT_FILE = {'type': 'file', 'src': 'less/variables.less', 'label': u'Variables'}
