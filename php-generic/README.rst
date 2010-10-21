How to localize your web application in 12 easy steps
=====================================================

#. ``cd your-app``

#. ``git clone git@github.com:stasm/webi18n.git ../webi18n``

#. ``cp -Rvn ../webi18n/php-generic/* . | grep "not overwritten"``

   If this shows something, make sure to resolve name conflicts manually.

#. ``cat htaccess-append.txt >> .htaccess``

   You may want to edit *.htaccess* next to make sure it looks fine.

#. Edit *includes/localization.php*.

   Change the value of the ``APPLICATION_ROOT`` constant if needed.

#. Edit *config/supported_locales.config.php*.

   Add the locales you want featured in your webapp.

#. Put the following like at the top of your code:

   ::

       include 'includes/localization.php';

   The exact path might vary.

   This will make a ``$locale`` variable available in your code. Use it to fix 
   those URLs! :)

#. Wrap every English string or message in gettext's ``_()`` function.

   This might end up being a lot of work. See these docs for help on using 
   gettext functions:

   * https://developer.mozilla.org/en/Web_Localizability
   * http://php.net/manual/en/book.gettext.php
   * https://developer.mozilla.org/en/gettext


#. Read *locale/README*.

   This will make you familiar with the localization process.

   In particular, please edit the *locale/meta.config.sh* file as described in
   *locale/README*.

#. ``./locale/extract.sh .``

   This will extract all localizable strings marked with gettext's `_()` 
   function family and put them in *locale/templates/LC_MESSAGES/messages.pot*.

#. ``./locale/add_locale.sh pl pl_PL.utf8``

   This will create the localization files (*\*.po*) for the localizers to work
   with. The files will be localed in *locale/pl/LC_MESSAGES/*. Distribute them
   to the localizers. 

   Rinse and repeat for every locale you want to add. 

   Invoke *locale/add_locale.sh* without any arguments to see help.

#. ``./locale/compile.sh``

   When the localization is completed, issue this to compile the *\*.po* files 
    to *\*.mo* files. These are used by the actual gettext module on the server.

    It's usually a good idea to hok the *locale/compile.sh* script to a cronjob
    running every 15 minutes or so on the staging server, together with an 
    ``svn update`` of the repository with the localization files. It's also 
    recommended not to do this on the production server.

