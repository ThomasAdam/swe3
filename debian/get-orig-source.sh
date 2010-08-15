#!/bin/sh

set -e

URL='https://smoothwall.svn.sourceforge.net/svnroot/smoothwall/trunk/distrib/build/sources/coretree/tree'

REV=$(svn info $URL | sed -ne 's/Last Changed Rev: \(.*\)$/\1/p')

TMPDIR=swe3_0.0~svn$REV

svn export $URL $TMPDIR
tar czf swe3_0.0~svn$REV.orig.tar.gz \
	--exclude=jta25.jar \
	--exclude=usr/ssl \
	$TMPDIR
rm -rf $TMPDIR
