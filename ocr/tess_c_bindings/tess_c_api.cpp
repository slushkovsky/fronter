#include "tess_c_api.h"
#include <leptonica/allheaders.h>

TessApi::TessApi(){
    api = new tesseract::TessBaseAPI();

    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
    }
}

TessApi::~TessApi(){
    api->End();
    delete api;
}

PyObject* TessApi::get_words(std::string imagepath)
{
    // Open input image with leptonica library
    Pix *image = pixRead(imagepath.c_str());

    api->SetImage(image);
    api->Recognize(0);
    tesseract::ResultIterator* ri = api->GetIterator();

    PyObject *words = PyList_New(0);

    if (ri != 0) {
        do {
            const char* word = ri->GetUTF8Text(tesseract::RIL_WORD);
            if (word != 0) {
                const char *font_name;
                bool bold, italic, underlined, monospace, serif, smallcaps;
                int pointsize, font_id;
                font_name = ri->WordFontAttributes(&bold, &italic, &underlined,
                                                   &monospace, &serif,
                                                   &smallcaps, &pointsize,
                                                   &font_id);

                PyObject *wordPy = PyDict_New();
                PyDict_SetItem(wordPy, PyUnicode_FromString("word"),
                               PyUnicode_FromString(word));
                PyDict_SetItem(wordPy, PyUnicode_FromString("font_name"),
                               PyUnicode_FromString(font_name));
                PyDict_SetItem(wordPy, PyUnicode_FromString("bold"),
                               PyBool_FromLong(bold));
                PyDict_SetItem(wordPy, PyUnicode_FromString("italic"),
                               PyBool_FromLong(italic));
                PyDict_SetItem(wordPy, PyUnicode_FromString("underlined"),
                               PyBool_FromLong(underlined));
                PyDict_SetItem(wordPy, PyUnicode_FromString("monospace"),
                               PyBool_FromLong(monospace));
                PyDict_SetItem(wordPy, PyUnicode_FromString("serif"),
                               PyBool_FromLong(serif));
                PyDict_SetItem(wordPy, PyUnicode_FromString("smallcaps"),
                               PyBool_FromLong(smallcaps));
                PyDict_SetItem(wordPy, PyUnicode_FromString("pointsize"),
                               PyLong_FromLong(pointsize));
                PyDict_SetItem(wordPy, PyUnicode_FromString("font_id"),
                               PyLong_FromLong(font_id));

                PyList_Append(words, wordPy);
            }
            delete[] word;
        } while (ri->Next(tesseract::RIL_WORD));
    }
    delete ri;
    pixDestroy(&image);

    return words;
}
