FROM rocker/shiny:4.0.5

# Install system requirements
# Clear cache first to get apt-get update working in case of outdated image
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get install -y \
    --no-install-recommends \
    libcurl4-gnutls-dev \
    libssl-dev \
    libxml2-dev \
    libicu-dev \
    libudunits2-dev \
    libproj-dev \
    libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV _R_SHLIB_STRIP_=true

RUN install2.r --error --skipinstalled --ncpu -1 \
    shiny \
    bsplus \
    readr \
    tidyverse \
    magrittr \
    sf \
    lubridate \
    leaflet \
    htmltools \
    htmlwidgets \
    ggplot2 \
    lwgeom \
    RColorBrewer \
    mapview \
    webshot \
    ggforce \
    DT

# Remove the samples:
RUN rm -rf /srv/shiny-server/*

COPY ./gnm_shiny_app/ /srv/shiny-server/

RUN chown shiny:shiny -R /srv/shiny-server

USER shiny

CMD ["/usr/bin/shiny-server"]
