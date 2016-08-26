#ifndef TESS_C_API_H
#define TESS_C_API_H

#include <tesseract/baseapi.h>
#include <string>
#include <Python.h>

class TessApi {

public:
    TessApi();
    ~TessApi();

    PyObject *get_words(std::string imagepath);

protected:
    tesseract::TessBaseAPI *api;

};

#endif // TESS_C_API_H
