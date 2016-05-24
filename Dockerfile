FROM php:5.6-fpm

# Install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        libgd3 \
        libgmp-dev \
        libicu-dev \
        libmemcached-dev \
        libpng12-dev \
        librabbitmq-dev \
        libssl-dev \
        libxext6 \
        libxrender1 \
        zlib1g-dev \
        && \
    rm -rf /var/lib/apt/lists/*

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer


RUN ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h


# Configure php & php-fpm
ENV PHP_INI /usr/local/etc/php/php.ini
ENV PHP_FPM /usr/local/etc/php-fpm.conf

# Install custom php extensions
RUN docker-php-ext-install exif gd gmp intl mbstring pcntl pdo_mysql zip


# Install pecl packages
RUN pecl config-set php_ini ${PHP_INI}
RUN yes | pecl install amqp-1.4.0 memcache sundown-0.3.11


RUN echo "" >> ${PHP_INI} && \
    
    echo "cgi.fix_pathinfo=0" >> ${PHP_INI}  && \
    
    echo "date.timezone=Europe/Paris" >> ${PHP_INI}  && \
    
    echo "extension=amqp.so" >> ${PHP_INI}  && \
    
    echo "extension=memcache.so" >> ${PHP_INI}  && \
    
    echo "extension=sundown.so" >> ${PHP_INI} 
    RUN echo "" >> ${PHP_FPM} \
    
    echo "catch_worker_output = yes" >> ${PHP_FPM}  && \
    
    echo "group = 1000" >> ${PHP_FPM}  && \
    
    echo "request_terminate_timeout = 300" >> ${PHP_FPM}  && \
    
    echo "user = 1000" >> ${PHP_FPM} 
    

# Create the source directory and set it as the working directory
ENV SRC_DIR /usr/src/app/
RUN mkdir -p ${SRC_DIR}
WORKDIR ${SRC_DIR}

# Install dependencies
COPY ./composer.* ${SRC_DIR}
RUN php -d memory_limit=-1 /usr/local/bin/composer global require --prefer-dist hirak/prestissimo && \
    php -d memory_limit=-1 /usr/local/bin/composer install --no-dev --prefer-dist --no-scripts && \
    rm -rf ~/.composer


RUN pecl install xdebug && echo "xdebug.remote_enable=1\nxdebug.remote_connect_back=1" >> ${PHP_INI} 


# Copy source code
COPY . ${SRC_DIR}

# Copy default parameters file
RUN cp app/config/parameters.yml.dist app/config/parameters.yml

# In order to avoid permission issues
RUN chown -R www-data:www-data ${SRC_DIR}

# Should always be the last !
VOLUME ${SRC_DIR}