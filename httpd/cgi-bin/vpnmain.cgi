#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use smoothtype qw( :standard );

my (%cgiparams,%checked);
my $filename = "${swroot}/vpn/config";

$cgiparams{'ENABLED'} = 'off';
&getcgihash(\%cgiparams);

my $errormessage = '';

if ($cgiparams{'ACTION'} eq $tr{'save'})
{
	if ($cgiparams{'VPN_IP'})
	{
		unless (&validip($cgiparams{'VPN_IP'})) {
			$errormessage = $tr{'invalid input'}; }
	}
	if ($errormessage) {
		$cgiparams{'VALID'} = 'no'; }
	else {
		$cgiparams{'VALID'} = 'yes'; }

	&writehash("${swroot}/vpn/settings", \%cgiparams);
}
&readhash("${swroot}/vpn/settings", \%cgiparams);

if ($cgiparams{'ACTION'} eq $tr{'restart'})
{
	system('/usr/bin/smoothwall/writeipsec.pl');

	my $success = message('ipsecrestart');
	
	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'}; }
}
if ($cgiparams{'ACTION'} eq $tr{'stop'})
{
	my $success = message('ipsecstop');
	
	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'}; }
}

if ($cgiparams{'VALID'} eq '')
{
        $cgiparams{'ENABLE'} = 'off';
}

$checked{'ENABLED'}{'off'} = '';
$checked{'ENABLED'}{'on'} = '';
$checked{'ENABLED'}{$cgiparams{'ENABLED'}} = 'CHECKED';

&showhttpheaders();

&openpage($tr{'vpn configuration main'}, 1, '', 'vpn');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'manual control and status'});
open (FILE, "$filename");
my @current = <FILE>;
close (FILE);

open (ACTIVE, "/proc/net/ipsec_eroute");
my @active = <ACTIVE>;
close (ACTIVE);

print <<END
<br/>
<table class='centered' style='width: 60%;'>
END
;

my $id = 0;
my $line;

# 0          192.168.0.0/24     -> 192.168.0.0/16     => tun0x1002@82.69.176.133

foreach $line (@current)
{
	$id++;
	chomp($line);
	my @temp = split(/\,/,$line);
	my $name = $temp[0];
	my $netmaskl = $temp[2];
	$netmaskl =~ /\//; $netmaskl = $`;
	my $netmaskr = $temp[4];
	$netmaskr =~ /\//; $netmaskr = $`;
	my $active = "<img src='/ui/img/closed.jpg' alt='$tr{'capsclosed'}'>";
	if ($temp[6] eq 'off') {
		$active = "<img src='/ui/img/disabled.jpg' alt='$tr{'capsdisabled'}'>";
	}

	foreach $line (@active)
	{
		@temp = split(/[\t ]+/,$line);
		$d = 0;
		$targetl = $temp[1];
		$targetl =~ /\//; $targetl = $`;
		$targetr = $temp[3];
		$targetr =~ /\//; $targetr = $`;
		if (($targetl eq $netmaskl && $targetr eq $netmaskr) ||
			($targetl eq $netmaskr && $targetr eq $netmaskl))
		 {
			$active = "<img src='/ui/img/open.jpg' alt='$tr{'capsopen'}'>";
		}
	}
	print "<tr class='dark' style='border: 1px solid #c0c0c0;'>\n"; 
	print "<td style='width: 65%; text-align: center;'><strong>$name</strong></td><td style='text-align: left;'>$active</td>\n";
	print "</tr><tr><td>&nbsp;</td></tr>\n";
}
print "</table>\n";
print <<END
<table class='blank'>
<tr>
<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'restart'}'></td>
<td style='width: 50%; text-align: center;'><input type='submit' name='ACTION' value='$tr{'stop'}'></td>
</tr>
</table>
<br/>
END
;

&closebox();

&openbox($tr{'global settingsc'});
print <<END
<TABLE WIDTH='100%'>
<TR>
<TD WIDTH='25%' CLASS='base'>$tr{'local vpn ip'}&nbsp;<IMG SRC='/ui/img/blob.gif'></TD>
<TD WIDTH='25%' ><INPUT TYPE='TEXT' NAME='VPN_IP' VALUE='$cgiparams{'VPN_IP'}' SIZE='15' id='vpn_ip' @{[jsvalidip('vpn_ip')]}></TD>
<TD WIDTH='25%' CLASS='base'>$tr{'enabled'}<INPUT TYPE='CHECKBOX' NAME='ENABLED' $checked{'ENABLED'}{'on'}></TD>
<TD WIDTH='25%' ALIGN='CENTER'><INPUT TYPE='SUBMIT' NAME='ACTION' VALUE='$tr{'save'}'></TD>
</TR>
</TABLE>
<BR>
<IMG SRC='/ui/img/blob.gif' VALIGN='top'>&nbsp;
<FONT CLASS='base'>$tr{'if blank the currently configured ethernet red address will be used'}</FONT>
END
;
&closebox();

&alertbox('add','add');

&closebigbox();

&closepage();
