#Imagen base de PHP con Apache
FROM php:8.3-apache

# Instalar utilidades necesarias (git, unzip, zip, curl)
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    zip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Activar extensiones comunes de PHP (puedes agregar más si las necesitas)
RUN docker-php-ext-install pdo pdo_mysql

# Instalar Composer globalmente
RUN curl -sS https://getcomposer.org/installer | php \
    && mv composer.phar /usr/local/bin/composer \
    && chmod +x /usr/local/bin/composer

# Establecer el directorio de trabajo
WORKDIR /var/www/html

# Copiar el contenido del proyecto al contenedor
COPY . /var/www/html

# Exponer el puerto de Apache
EXPOSE 80

# Iniciar Apache
CMD ["apache2-foreground"]