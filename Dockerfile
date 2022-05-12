FROM httpd:2.4

# This follows the steps documented here: https://cwiki.apache.org/confluence/display/KAFKA/Setup+Kafka+Website+on+Local+Apache+Server
RUN sed -i \
  -e 's/#LoadModule include_module modules\/mod_include.so/LoadModule include_module modules\/mod_include.so/g' \
  -e 's/#LoadModule rewrite_module modules\/mod_rewrite.so/LoadModule rewrite_module modules\/mod_rewrite.so/g' \
  -e '/^DocumentRoot/,/AllowOverride None/s/AllowOverride None/AllowOverride All/' \
  "/usr/local/apache2/conf/httpd.conf"

CMD ["httpd-foreground"]
