[![Build Status](https://travis-ci.org/patissiere/muffin.svg?branch=master)](https://travis-ci.org/patissiere/muffin)

# Muffin
Muffin is a structured reporting solution for test results

# API Spec

We follow the guidelines specified here:
http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api

- Each endpoint should be clearly documented in which fields it supports filtering on, 
pass the query to filter as a json object in the filter argument.
- Each endpoint should support selecting which fields to return using a 
comma separated fields attribute
- We never return naked arrays as the top level object, return the pluralized form of 
the resource you are working on.
- Patch endpoints accept json patch objects or return 403 if run on a 
field / the operation is not allowed
