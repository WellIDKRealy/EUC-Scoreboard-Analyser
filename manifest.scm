(use-modules (guix packages)
	     (guix download)
	     (guix git-download)
	     (guix build-system python)
	     (guix build-system pyproject)
	     (gnu packages python-xyz)
	     (gnu packages ocr)
	     (gnu packages machine-learning)
	     (gnu packages image-processing)
	     (gnu packages python-science)
	     (gnu packages check)
	     (gnu packages python-check)
	     (gnu packages ninja)
	     ((guix licenses)
	      #:prefix license:))

(define python-pytest-virtualenv
  (package
   (name "python-pytest-virtualenv")
   (version "1.7.0")
   (source
    (origin
     (method url-fetch)
     (uri (pypi-uri "pytest-virtualenv" version))
     (sha256
      (base32 "03w2zz3crblj1p6i8nq17946hbn3zqp9z7cfnifw47hi4a4fww12"))))
   (build-system pyproject-build-system)
   (propagated-inputs (list python-pytest
			    python-pytest-fixture-config
			    python-pytest-shutil
			    python-virtualenv))
   (native-inputs (list python-mock))
   (home-page "https://github.com/manahl/pytest-plugins")
   (synopsis "Virtualenv fixture for py.test")
   (description "Virtualenv fixture for py.test")
   (license license:expat)))

(define python-ninja
  (package
   (name "python-ninja")
   (version "1.11.1.1")
   (source
    (origin
     (method url-fetch)
     (uri (pypi-uri "ninja" version))
     (sha256
      (base32 "0g6c2xhdn36a0m4s1znw89d4hz2x2jvydsgznv83hzl5vl43nycx"))))
   (build-system pyproject-build-system)
   (native-inputs (list python-codecov
			python-coverage
			python-flake8
			python-pytest
			python-pytest-cov
			python-pytest-runner
			python-pytest-virtualenv
			python-virtualenv
			python-scikit-build
			ninja))
   (home-page "http://ninja-build.org/")
   (synopsis "Ninja is a small build system with a focus on speed")
   (description "Ninja is a small build system with a focus on speed")
   (license license:asl2.0)))

(define python-pytesseract
  (package
   (name "python-pytesseract")
   (version "0.3.10")
   (source
    (origin
     (method url-fetch)
     (uri (pypi-uri "pytesseract" version))
     (sha256
      (base32 "03qjshmsdivdsjb6fyjpsp0yxrjv66wgalflhl81ml3zy2qaihzi"))))
   (build-system pyproject-build-system)
   (propagated-inputs (list python-packaging
			    python-pillow
			    tesseract-ocr))
   (home-page "https://github.com/madmaze/pytesseract")
   (synopsis "Python-tesseract is a python wrapper for Google's Tesseract-OCR")
   (description
    "Python-tesseract is a python wrapper for Google's Tesseract-OCR")
   (license #f)))

(define python-easyocr
  (package
   (name "python-easyocr")
   (version "1.7.1")
   (source
    (origin
     (method git-fetch)
     (uri (git-reference
	   (url "https://github.com/JaidedAI/EasyOCR.git")
	   (commit "v1.7.1")))
     (sha256
      (base32 "0hpm1jwjvlhy1njrdv5q6s8pk9dd9ipcnxpph0pq5fbpnbc8ja0j"))))
   (build-system pyproject-build-system)
   (propagated-inputs
    (list python-packaging
	  python-pillow
	  python-pytorch
	  python-torchvision
	  opencv
	  python-scipy
	  python-numpy
	  python-scikit-image
	  python-pyyaml
	  python-shapely
	  python-pyclipper
	  python-ninja
	  tesseract-ocr))
   (home-page "https://github.com/madmaze/pytesseract")
   (synopsis "Python-tesseract is a python wrapper for Google's Tesseract-OCR")
   (description
    "Python-tesseract is a python wrapper for Google's Tesseract-OCR")
   (license #f)))

(packages->manifest
 (cons* python-pytesseract
	;; python-easyocr
	(specifications->packages
	 '("python"
	   "opencv"
	   "python-numpy"
	   "coreutils"
	   "inetutils"))))
