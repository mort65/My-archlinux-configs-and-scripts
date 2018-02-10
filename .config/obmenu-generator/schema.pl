#!/usr/bin/perl

# obmenu-generator - schema file

=for comment

    item:      add an item inside the menu               {item => ["command", "label", "icon"]},
    cat:       add a category inside the menu             {cat => ["name", "label", "icon"]},
    sep:       horizontal line separator                  {sep => undef}, {sep => "label"},
    pipe:      a pipe menu entry                         {pipe => ["command", "label", "icon"]},
    file:      include the content of an XML file        {file => "/path/to/file.xml"},
    raw:       any XML data supported by Openbox          {raw => q(xml data)},
    begin_cat: begin of a category                  {begin_cat => ["name", "icon"]},
    end_cat:   end of a category                      {end_cat => undef},
    obgenmenu: generic menu settings                {obgenmenu => ["label", "icon"]},
    exit:      default "Exit" action                     {exit => ["label", "icon"]},

=cut

# NOTE:
#    * Keys and values are case sensitive. Keep all keys lowercase.
#    * ICON can be a either a direct path to an icon or a valid icon name
#    * Category names are case insensitive. (X-XFCE and x_xfce are equivalent)

require "$ENV{HOME}/.config/obmenu-generator/config.pl";

## Text editor
my $editor = $CONFIG->{editor};

our $SCHEMA = [

    #          COMMAND                 LABEL              ICON
    {item => ['xdg-open .',       'File Manager', 'system-file-manager']},
    {item => ['lxterminal',            'Terminal',     'utilities-terminal']},
    {item => ['xdg-open https://www.archlinux.org/', 'Web Browser',  'web-browser']},
    {item => ['gmrun',            'Run Program',  'system-run']},
    {sep  => undef},
    {pipe => ['~/bin/openbox/obrecent.sh',              'Recent Documents',  'document-open-recent']},

    #{sep => 'Categories'},
    {sep  => undef},

    #          NAME            LABEL                ICON
    {cat => ['utility',     'Accessories', 'applications-utilities']},
    {cat => ['development', 'Development', 'applications-development']},
    {cat => ['education',   'Education',   'applications-science']},
    {cat => ['game',        'Games',       'applications-games']},
    {cat => ['graphics',    'Graphics',    'applications-graphics']},
    {cat => ['audiovideo',  'Multimedia',  'applications-multimedia']},
    {cat => ['network',     'Network',     'applications-internet']},
    {cat => ['office',      'Office',      'applications-office']},
    {cat => ['other',       'Other',       'applications-other']},
    {cat => ['settings',    'Settings',    'applications-accessories']},
    {cat => ['system',      'System',      'applications-system']},

    #                  LABEL          ICON
    #{begin_cat => ['My category',  'cat-icon']},
    #             ... some items ...
    #{end_cat   => undef},

    #            COMMAND     LABEL        ICON
    #{pipe => ['obbrowser', 'Disk', 'drive-harddisk']},

    ## Generic advanced settings
    #{sep       => undef},
    #{obgenmenu => ['Openbox Settings', 'applications-engineering']},
    #{sep       => undef},

    ## Custom advanced settings
    {sep       => undef},
    {begin_cat => ['Advanced Settings', 'applications-engineering']},
	#Appearance
        {item      => ["/usr/bin/lxappearance", 'Look and Feel',   'cs-cat-appearance']},
      #Wallpaper
      {item => ["/usr/bin/nitrogen",              'Wallpaper Setter',    'preferences-desktop-wallpaper']},

     #{begin_cat => ['Fbpanel',  'system-settings']},
     
      # Configuration editor
      #{item => ['fbpanel -C',              'Fbpanel Config',    'system-settings']},
     
      # Configuration files
      #{item => ["$editor ~/.config/fbpanel/default", 'Fbpanel Panel Top', 'text-x-generic']},
      #{item => ["$editor ~/.config/fbpanel/tasks", 'Fbpanel Panel Bottom',    'text-x-generic']},
      
     #{end_cat => undef},
     
     {begin_cat => ['jgmenu', 'start-here']},
     
      # Configuration editor
      {item => ['killall jgmenu', 'Restart jgmenu', 'start-here']},
     
      # Configuration files
      {item => ["$editor ~/.config/jgmenu/prepend.csv", 'Jgmenu Prepend',    'text-x-generic']},
      {item => ["$editor ~/.config/jgmenu/jgmenurc", 'Jgmenu Config', 'text-x-generic']},
      {item => ["$editor ~/.config/jgmenu/append.csv", 'Jgmenu Append',    'text-x-generic']},
      
     {end_cat => undef},
     
     {begin_cat => ['Tint2', 'tint2']},
     
      # Configuration editor
      {item => ['tint2conf',              'Tint2 Config',    'tint2conf']},
     
      # Configuration files
      {item => ["$editor ~/.config/tint2/tint2rc", 'Tint2 Panel', 'text-x-generic']},
      #{item => ["$editor ~/.config/tint2/tint2tasks", 'Tint2 Panel Bottom',    'text-x-generic']},
      
     {end_cat => undef},
     
      # obmenu-generator category
      {begin_cat => ['Obmenu-Generator', 'accessories-text-editor']},
        {item      => ["$editor ~/.config/obmenu-generator/schema.pl", 'Menu Schema', 'text-x-generic']},
        {item      => ["$editor ~/.config/obmenu-generator/config.pl", 'Menu Config', 'text-x-generic']},

        {sep  => undef},
        {item => ['obmenu-generator -s -c',    'Generate a static menu',             'accessories-text-editor']},
        {item => ['obmenu-generator -s -i -c', 'Generate a static menu with icons',  'accessories-text-editor']},
        {sep  => undef},
        {item => ['obmenu-generator -p',       'Generate a dynamic menu',            'accessories-text-editor']},
        {item => ['obmenu-generator -p -i',    'Generate a dynamic menu with icons', 'accessories-text-editor']},
        {sep  => undef},

        {item    => ['obmenu-generator -d', 'Refresh Icon Set', 'view-refresh']},
      {end_cat => undef},

      # Openbox category
      {begin_cat => ['Openbox', 'openbox']},
        {item      => ["/usr/bin/obconf", 'Openbox Config',   'obconf']},
        {item      => ["$editor ~/.config/openbox/autostart", 'Openbox Autostart',   'text-x-generic']},
        {item      => ["$editor ~/.config/openbox/rc.xml",    'Openbox RC',          'text-x-generic']},
        {item      => ["$editor ~/.config/openbox/menu.xml",  'Openbox Menu',        'text-x-generic']},
        {item      => ['openbox --reconfigure',               'Reconfigure Openbox', 'openbox']},
     {end_cat => undef},
     {sep => undef},
      # Exit category
      {begin_cat => ['Exit', 'application-exit']},
        {item      => ['openbox --exit', 'Logout', 'system-log-out']},
        {item      => ['systemctl reboot', 'Restart', 'system-reboot']},
	{item      => ['systemctl suspend', 'Suspend', 'system-suspend']},
        {item      => ['systemctl hibernate', 'Hibernate', 'system-hibernate']},
        {item      => ['systemctl poweroff', 'Shutdown', 'system-shutdown']},
      {end_cat => undef},
    {end_cat => undef},

    {sep => undef},

    ## This uses the 'oblogout' menu
    {item => ['oblogout', 'Exit', 'exit']},
]
