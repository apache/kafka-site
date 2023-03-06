FROM httpd:2.4

# This follows the steps documented here: https://cwiki.apache.org/confluence/display/KAFKA/Setup+Kafka+Website+on+Local+Apache+Server
RUN sed -i \
  -e 's/#LoadModule include_module modules\/mod_include.so/LoadModule include_module modules\/mod_include.so/g' \
  -e 's/#LoadModule rewrite_module modules\/mod_rewrite.so/LoadModule rewrite_module modules\/mod_rewrite.so/g' \
  -e 's/Options Indexes FollowSymLinks/Options +Includes/g' \
  -e '/<Directory "\/usr\/local\/apache2\/htdocs">/a\    RewriteEngine On\
      AddType text/html .html\n\
      AddHandler server-parsed .html\n\
      Redirect 301 /design.html /documentation#design\n\
      RewriteRule ^/?(\d+)/generated/ - [S=4]\n\
      RewriteRule ^/?(\d+)/documentation(\.html)? - [S=3]\n\
      RewriteRule ^/?(\d+)/javadoc - [S=2]\n\
      RewriteRule ^/?(\d+)/images/ - [S=1]\n\
      RewriteCond $2 !=protocol\n\
      RewriteRule ^/?(\d+)/([a-z]+)(\.html)? /$1/documentation#$2 [R=302,L,NE]\n\
      RewriteCond %{REQUEST_FILENAME}.html -f\n\
      RewriteRule ^(.*)$ %{REQUEST_FILENAME}.html' \
  "/usr/local/apache2/conf/httpd.conf"

CMD ["httpd-foreground"]
