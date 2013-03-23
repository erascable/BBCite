# ---------------------------------------------------------------------------- #
#			     	  B B C I T E 				       #
# 									       #
# This script breaks down cases and adds the correct tags. Needs to handle     #
# footnotes citations such as '536 A.2d 1337 n. 4' and citations with flags in #
# them referencing dispositions 'appeal denied, 519 Pa. 667, (1988)'. 	       #
# 									       #
# The original works by looking for the date '(\d\d\d\d)', then building XML   #
# tags around the found piece of citation, and then running through the file   #
# again with a different regular expression, again adding XML as it goes. In   #
# this way it works from right to left to build up a citation. 		       #
# 									       #
# Converts: 								       #
# 									       #
# "Lorem ipsum dolor sit amet, consectetur dipiscing elit. Weems v.Citigroup,  #
# Inc., 289 Conn. 769 (2008)." 						       #
# 									       #
# Into the following: 							       #
# 									       #
# <para> Lorem ipsum dolor sit amet, consectetur adipiscing elit 	       #
#        <bibliolist><bibliomixed> 					       #
#                <title role="casename">Weems v. Citigroup, Inc.</title>,      #
#                        <bibliomisc> 					       #
#                                <citation>289 Conn. 769</citation> 	       #
#                                <phrase role="dept_and_year">(2008)</phrase>  #
#                        </bibliomisc>  				       #
#        </bibliomixed></bibliolist> 					       #
# .</para> 								       #
# ---------------------------------------------------------------------------- #

# TODO: etree / lxml to make the xml parts look nicer.

<<<<<<< HEAD
import re
=======
>>>>>>> General cleaning and formatting
import datetime
import fileinput
import os
import re
import sys
# import xml.etree.ElementTree as ET

# bibliolist = Element('bibliolist')
# bibliomixed = SubElement(bibliolist, 'bibliomixed')
# title = SubElement(bibliomixed, 'title')
# title.set('role', 'casename')
# bibliomisc = SubElement(title, 'bibliomisc')
# citation = SubElement(bibliomisc, 'citaton')
# phrase = SubElement(bibliomisc, 'phrase')
# phrase.set('role', dept_and_year')

<<<<<<< HEAD
targetfile = 'test.xml'
os.rename(os.path.realpath(targetfile), os.path.realpath(targetfile)+'.xml~')
f = open(os.path.realpath(targetfile), 'w')

=======
# targetfile = 'FILE.xml'
# os.rename(os.path.realpath(targetfile), os.path.realpath(targetfile)+'.xml~')
# f = open(os.path.realpath(targetfile), 'w')

# with open(f, 'w')
#     data = file.readlines()

>>>>>>> General cleaning and formatting
# ---------------------------------------------------------------------------- # 
# File manipulation
# ---------------------------------------------------------------------------- # 

for line in f:

    if not line:
        break

    # TODO: compile all of these regexes into nicer forms. 
    line.replace(' vs. ', ' v. ')

    # Tag the <phrase>. 
    # The leading '(\d )' ensures that we exclude things like '(Exhibit T. 1732)' 
    # by looking for the end of the case citation before it.
    re.sub(r'\d,?) (\([\w,\'\. ]*\d{4}\))([\.;, ]?])', 
			'\1<phrase role="dept_and_year">\2</phrase>\3', 'line')

    # Tag any cases already tagged with a <phrase> with <citation> and 
    # <citation role="parallel_citation">. Semicolon catches ';' in '&amp;'. 
    # The '\*' asterisk catches those star cites (*7) that copypasta attorneys 
    # like to use from Lexis.
    re.sub(r', ([\d_]+ [\w#&;\. ]+ [\d_\*\- ]+), ([\d_]+ [\w#&;\. ]+ [\d_\*\- ]+) <phrase', 
			', <citation>\1</citation>, <citation role="parallel_citation">\2</citation> <phrase>', 'line')

    # Tag the <citation> (without parallel cites). Will catch trailing pinpoint
    # citations.
    re.sub(r', ([\d_]* [\w#&;\.\- ]* [\d_#&;,\- ]*) <phrase', 
			', <citation>\1</citation> <phrase', 'line')

    # Tag the <citation> for citing footnotes.
    re.sub(r', ([\d_]+ [\w#&;\. ]+ [\d_\-]+ [Nn]\.[\d]*) <phrase', 
			', <citaiton>\1</citation> <phrase', 'line')

    # Tag citation and phrase with <bibliomisc>. The \{-} is important, otherwise
    # the search is too greedy and finds whole paragraph.
    re.sub(r'<citation>.+?</phrase>', '<bibliomisc>\1</bibliomisc>', 'line')

    # Tag the <title>. This regex looks for a string of words that have leading 
    # capitol letters followed by a 'v.' and terminates on the following 
    # <bibliomisc> tag. While this catches plaintiffs with multiple names, it will
    # catch the 'When' in 'When Frank Rizzo, Inc. v. Foo was decided . . .' These
    # false positives are removed by later regexs. This algorithm will miss
    # 'Insurance Society of' in 'Insurance Society of Pennsylvania' or the ''t' in
    # case names like ''t Hooft v. Smith' because it is looking for a string
    # of capitalized words.
    re.sub(r'(([A-Z][\w,\-\.\(\)\'#&;]+ )+)v\. ([\w,\-\.\(\)\'#&; ]+), <bibliomisc', 
			'<title role="casename">\1v. \3</title>, <bibliomisc', 'line')

# ---------------------------------------------------------------------------- # 
# Special Cases
# ---------------------------------------------------------------------------- # 

    # Finds and tags with <title> 'In re Foo'.
    re.sub(r'[Ii]n [Rr]e [\w\' ]+), <bibliomisc', 
			'<title role="casename">\1</title>, <bibliomisc', 'line')
    # Finds and tags 'Ex rel. Foo'.
    re.sub(r'[Ee]x [Rr]el.? [\w\' ]+), <bibliomisc', 
			'<title role="casename">\1</title>, <bibliomisc', 'line')
# ---------------------------------------------------------------------------- #
# Removing incorrectly tagged words, mostly because they lead a sentence and 
# are capitalized.
# Emphasizes flags.
# ---------------------------------------------------------------------------- #

    # Removes wrongly found 'In' ('In Foo v. Bar . . .', 'line') from citation titles without messing up 'In re' cases.
    re.sub(r'<title role="casename">(In (?![Rr]e))', 
			'In <title role="casename">', 'line')

    # As above, with 'When'
    re.sub(r'<title role="casename">When ', 'When <title role="casename">', 'line')

    # As above, with 'Yes. '
    re.sub(r'<title role="casename">Yes ', 'Yes <title role="casename">', 'line')

    # As above, with 'No. '
    re.sub(r'<title role="casename">No ', 'No <title role="casename">', 'line')

    # As above, with 'Contra'. Adds emphasis.
    re.sub(r'<title role="casename">Contra ', 
			'<emphasis role="italic">Contra</emphasis> <title role="casename">', 'line')

    # As above, with 'Accord'. Adds emphasis.
    re.sub(r'<title role="casename">Accord ', 
			'<emphasis role="italic">Accord</emphasis> <title role="casename">', 'line')

    # As above, with 'Compare'. Adds emphasis.
    re.sub(r'<title role="casename">Compare ', 
			'<emphasis role="italic">Compare</emphasis> <title role="casename">', 'line')

    # As above, with 'However,'. Adds emphasis.
    re.sub(r'<title role="casename">However ', 
			'<emphasis role="italic">However</emphasis> <title role="casename">', 'line')

    # As above, with 'See'. Adds emphasis.
    re.sub(r'<title role="casename">See,? ', 
			'<emphasis role="italic">See</emphasis>, <title role="casename">', 'line')

    # As above, with 'Citing'. Adds emphasis.
    re.sub(r'<title role="casename">Citing ', 
			'<emphasis role="italic">Citing</emphasis> <title role="casename">', 'line')

# ---------------------------------------------------------------------------- #
# Finishes the tag
# Tag the whole citation with <bibliolist><bibliomixed>. The '\{-}' is
# important, prevents the RegEx from finding too much.
# ---------------------------------------------------------------------------- # 

    re.sub(r'<title role="casename">.*?</bibliomisc>', 
			'<bibliolist><bibliomixed>\1</bibliomixed></bibliolist>', 'line')

# ---------------------------------------------------------------------------- #
# More special cases, this time moving case names with necessarily variable 
# capitalization into the tag.
# ---------------------------------------------------------------------------- #

    # Moves missed 'ex rel.' into the title tag.
    re.sub(r'([Ee]x [Rr]el\. )<bibliolist>', '<bibliolist>\1', 'line')

    # Moves missed 'ex parte' into the title tag.
    # silent! %s!\([Ee]x [Pp]arte \)<bibliolist>!<bibliolist>\1 !g
    re.sub(r'([Ee]x [Pp]arte )<bibliolist>', '<bibliolist>\1', 'line')

# ---------------------------------------------------------------------------- #
# Emphasize flags
#
# The following list of flags is troublesome---each can be used in normal 
# discussion of a case, and would not be highlighted there:
#
# affirmed
# abrogated
# overruled by
# remanded
# vacated
# appeal denied
# ---------------------------------------------------------------------------- #

# But cf. and Cf.
# silent! %s!But, \([Cc]f\.\)!But \1!g
# silent! %s!\(But \)\=\([Cc]\)f\.!<emphasis role="italic">\1\2f.</emphasis>!g

# Correct I.d.
# silent! %s!I\.[Dd]\.!Id.!g

# Id.
# silent! %s!\<Id\.\>! <emphasis role="italic">&</emphasis>!g

# Ibid.
# silent! %s!Ibid\.!<emphasis role="italic">&</emphasis>!g

# Accord
# silent! %s!\<Accord\>!<emphasis role="italic">&</emphasis> <!g

# See, e.g.,
# silent! %s!See,\= e\.g\.,\=!<emphasis role="italic">See</emphasis>, <emphasis role="italic">e.g.</emphasis>,!g

# See also, 
# silent! %s![Ss]ee [Aa]lso,\=!<emphasis role="italic">See also</emphasis>,!g

# See also, e.g.,
# silent! %s![Ss]ee [Aa]lso,\= e\.g\.,!<emphasis role="italic">See also</emphasis>, <emphasis role="italic">e.g.</emphasis>,!g

# But see, e.g.,
# silent! %s!But [Ss]ee,\= e\.g\.,\=!<emphasis role="italic">But see</emphasis>, <emphasis role="italic">e.g.</emphasis>,!g

# aff'd
# silent! %s![Aa]ff'd!<emphasis role="italic">\L&\e</emphasis>!g

# aff'd per curiam
# silent! %s![Aa]ff'd per curiam!<emphasis role="italic">\L&\e</emphasis>!g

# cert. denied
# silent! %s![Cc]ert\. [Dd]enied!<emphasis role="italic">\L&\e</emphasis>!g

# cert. dismissed
# silent! %s![Cc]ert\. [Dd]ismissed!<emphasis role="italic">\L&\e</emphasis>!g

# mem.
# silent! %s!\<[Mm]em\.\>!<emphasis role="italic">\L&\e</emphasis>!g

# rev'd on other grounds
# silent! %s![Rr]ev'd on other grounds!<emphasis role="italic">\L&\e</emphasis>!g

# rev'd in banc and rev'd en banc
# silent! %s![Rr]ev'd [IiEe]n [Bb]anc!<emphasis role="italic">\L&\e</emphasis>!g

# rev'd
# silent! %s![Rr]ev'd!<emphasis role="italic">\L&\e</emphasis>!g

# ---------------------------------------------------------------------------- #
# Un-tags cases that we cannot actually link to, because they are in 
# proprietary LEXIS or WEST reporters.
# 
# To add:
# Pa. C
# Pa. D
# Pa. D. & C.
# Pa. D. & C.2nd
# Pa. D. & C.3rd
# And corrections for misspellings 
# ---------------------------------------------------------------------------- #

# Finds failed tags (LEXIS and WL, mostly ) and untags them . . .
# silent! %s#<phrase role="dept_and_year">\(([A-Za-z0-9,'\. ]*\d\d\d\d)\)<\/phrase>\(<\/bibliomisc>\)\@!#\1#g

# Finds failed title tags and untags them
# silent! %s#\(<bibliomixed>\)\@<!<title role="casename">\(\([A-Za-z,\-\.()'#;&]\+ \)*\)v\. \([A-Za-z0-9,\-\.()'#;& ]\+\)\)<\/title>#\2v. \4#g

# . . . and then tags them in italic
# silent! %s!\(\(\<[A-Z][A-Za-z,\-\.()'#;&]\+ \)*\)v\. \([A-Za-z0-9,\-\.()'#;& ]\+\), \(\d\+\) \(WL\|LEXIS\) \(\d\+\)[\., ]!<emphasis role="italic">\1v. \3</emphasis>, \4 \5 \6!g

# XML formatting
# silent! %s!\(<bibliolist><bibliomixed>.\{-}</bibliomixed></bibliolist>\)!\r\1!g
# silent! %s!\(<title.\{-}</title>, \)!\r\1!g
# silent! %s!\(<bibliomisc>.\{-}</bibliomisc>\)!\r\1!g
# silent! %s!\(<citation>.\{-}</citation> \)!\r\1!g
# silent! %s!\(<citation role="parallel_citation">.\{-}</citation> \)!\r\1!g
# silent! %s!\(<phrase.\{-}</phrase>\)!\r\1!g
# silent! %s!</bibliomisc>!\r&!g
# silent! %s!</bibliomixed></bibliolist>[\.,; ]!\r&\r!g

#    else:
#        break

with open ('test.txt', 'r') as f:
	data = file.readlines()

print data

data[2] = '<!-- Edited by BBCite on ', time.strftime(%Y : %m : %d : %H : %M : %S), ' -->\n'

with open('test.txt', 'w') as f:
	f.writelines( data )

f.close()
