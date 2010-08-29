#!/usr/bin/perl

use strict;
use warnings;

use Plack::Builder;
use Plack::App::CGIBin;
use Plack::App::File;

my $app = Plack::App::CGIBin->new(
	root => '/usr/share/swe3/html/cgi-bin/',
	exec_cb => sub { 1 },
);

my $static = Plack::App::File->new(
	root => '/usr/share/swe3/html/'
);

builder {
	mount "/cgi-bin/" => $app,
	mount "/" => $static,
};

