@ECHO OFF

REM Sync with Makefile

pushd %~dp0

REM Command file for Sphinx documentation

set PKGDIR=../src/citecheck

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
if "%SPHINXAPIDOC%" == "" (
	set SPHINXAPIDOC=sphinx-apidoc
)
set SOURCEDIR=source
set BUILDDIR=build
set APIDOCDIR=%SOURCEDIR%/_apidoc

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help


set SPHINX_APIDOC_OPTIONS=members,show-inheritance
%SPHINXAPIDOC% --force --separate --no-toc -o %APIDOCDIR% %PKGDIR%
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
