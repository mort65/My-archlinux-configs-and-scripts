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
    {item => ['mlterm',            'Terminal',     'utilities-terminal']},
    {item => ['xdg-open https://www.archlinux.org/', 'Web Browser',  'web-browser']},
    {item => ['gmrun',            'Run command',  'system-run']},

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
      #Wallpaper
      {item => ["/usr/bin/nitrogen",              'Wallpaper Setter',    'text-x-generic']},

     {begin_cat => ['Fbpanel']},
     
      # Configuration editor
      {item => ['fbpanel -C',              'Fbpanel Config',    'text-x-generic']},
     
      # Configuration files
      {item => ["$editor ~/.config/fbpanel/default", 'Fbpanel Panel Top', 'text-x-generic']},
      {item => ["$editor ~/.config/fbpanel/tasks", 'Fbpanel Panel Bottom',    'text-x-generic']},
      
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
        {item      => ["/usr/bin/obconf", 'Openbox Config',   'text-x-generic']},
        {item      => ["$editor ~/.config/openbox/autostart", 'Openbox Autostart',   'text-x-generic']},
        {item      => ["$editor ~/.config/openbox/rc.xml",    'Openbox RC',          'text-x-generic']},
        {item      => ["$editor ~/.config/openbox/menu.xml",  'Openbox Menu',        'text-x-generic']},
        {item      => ['openbox --reconfigure',               'Reconfigure Openbox', 'openbox']},
	{sep => undef},
      # Exit category
      {begin_cat => ['Exit', 'application-exit']},
        {item      => ['openbox --exit', 'Log Out', 'text-x-generic']},
        {item      => ['systemctl poweroff', 'Shutdown', 'text-x-generic']},
        {item      => ['systemctl reboot', 'Restart', 'text-x-generic']},
        {item      => ['systemctl suspend', 'Suspend', 'text-x-generic']},
        {item      => ['systemctl hibernate', 'Hibernate', 'text-x-generic']},
      {end_cat => undef},
     {end_cat => undef},
    {end_cat => undef},

    {sep => undef},

    ## The xscreensaver lock command
    #{item => ['xscreensaver-command -lock', 'Lock', 'system-lock-screen']},

    ## This option uses the default Openbox's action "Exit"
    ##{exit => ['Exit', 'application-exit']},
      # Exit category
      #{begin_cat => ['Exit', 'application-exit']},
      #  {item      => ['openbox --exit', 'Log Out', 'text-x-generic']},
      #  {item      => ['systemctl poweroff', 'Shutdown', 'text-x-generic']},
      #  {item      => ['systemctl reboot', 'Restart', 'text-x-generic']},
      #  {item      => ['systemctl suspend', 'Suspend', 'text-x-generic']},
      #  {item      => ['systemctl hibernate', 'Hibernate', 'text-x-generic']},
      #{end_cat => undef},

    ## This uses the 'oblogout' menu
    {item => ['oblogout', 'Exit', 'exit']},
]