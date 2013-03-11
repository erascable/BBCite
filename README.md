Citation-Parser
===============

This is *going* to be a python 2.x library that will pull apart and return various parts of Blue Book legal citations. It relies on a vicious admixture of RegExes and pure cunning, and is practice in python. The original script has been tested on thousands of citations, and performs better than the algo used by Lexis (but not better than West).


Status
======

Currently refactoring code so that it can do everything the original vim script can do.

Future
======

Will be able to identify and manipulate these elements:

# Standard Citations


Foo v. Bar, 123 AB.&C 456 (2002).
  Composition: casename, citation, date
Foo v. Bar, Inc., 123 ABC 456, 789 (1932);
	Composition: casename, citation, pinpoint citation, date
Foo O'Bar v. Bar, 123 ABC 456, 321 DEF2d. 678 (USSC 1999),
	Composition: casename, citation, parallel citation 1, date
Foo of Bar v. Bar, Inc, 123 ABC 456, n. *8 ('t Hooft, 1992),
	Composition: casename, citation, footnote citation, date
In re Bar, 789 ABC 987, 800, 123 DEF 456, 201, 222 GHI 333, 300 (remanded 1920);
	Composition: casename, citation, parallel citation 1, parallel citation 2, date
Foo v. Bar, 123 ABC 456 (D.C. Cir. 1983), rev'd 222 GHI 444 (1984).
	Composition: casename, citation, date, flag, clag citation, date
Foo, 123 ABC at 155 (1929).
	Composition: short casename, at citation, date
## Case name

Case names can be divided into smaller chunks, but are always ended in a comma.

Foo v. Bar,
Foo v. Bar, Inc.,
Insurance Society of Foo v. O'Bar,
	title(plaintiff, v, defendant)
		plaintiff('Foo')
		defendant('Bar', 'Bar, Inc.')
		v('v.', 'vs.', 'v', 'vs') [various capitulations]
In re Foo,
In regards to Foo,
In the matter of Foo,
Ex rel Bar,
Ex relatione Bar,
	latin_casename('In re', 'In the matter of', 'Ex rel', 'Ex rel.') [various capitalizations and punctuation]
	latin_casename(latin, name)
## Date
(1929)
(D.C Cir. 1983)
(Johnson, 1999)
	date(judge, disposition, department, year)
	date()
		year()
		department()
		judge()

## Citation

123 ABC 456,
456 BC.2d 987, 1000,
___ ABC ___,
789 ABC 987, 800, 123 DEF 456, 201, 222 GHI 333, 300
123 ABC 456 (1928), rev'd 456 BCA 987 (1929).

	citation(123 ABC 456)
		book(123)
		reporter(ABC)
		page(456)

	citation(456 BC.2d. 987, 1000)
		book(456)
		reporter(BC.2d)
		page(987)
		pinpoint_citation(1000)
	citation(___ ABC ___,)
		book(___)
		reporter(ABC)
		page(___)	

	citation(789 ABC 987, 800, 123 DEF 456, 201, 222 GHI 333, 300)
		book(789)
		reporter(ABC)
		page(987)
		pinpoint_citation(800)
		parallel_citation(123 DEF 456, 201)
			book()
			reporter()
			page()
			pinpoint_citation()
		parallel_citation_2()
			book()
			reporter()
			page()
			pinpoint_citation()

	citation(123 ABC 456 (1928), rev'd 456 BCA 987 (1929).)
			book(123)
			reporter(ABC)
			page(456)
		date(1928)
			disposition(rev'd)
			book(456)
			reporter(BCA)
			page(987)
		date(1929)	

## Better taxonomy

Need to add: Opinion Description, Flags, Subsequent History, and Prior History

def citation():
	title
		plaintiff
		defendant
	citation
		book
		reporter
		page
		pinpoint
		note
	citation_2
		book
		reporter
		page
		pinpoint
		note
	citation_3
		book
		reporter
		page
		pinpoint
		note
	date
		department
		judge
		year
	capsule_summary
	flag
		subsequent_history
	flag_2
		subsequent_history
	flag_3
		subsequent_history
	flag_a
		prior_history
	flag_b
		prior_history
	flag_c
		prior_history
	
def latin_citation():
	title
		name
	citation
		book
		reporter
		page
		pinpoint
		note
	citation 2
		book
		reporter
		page
		pinpoint
		note
	citation 3
		book
		reporter
		page
		pinpoint
		note
	date
		department
		judge
		year

def short_citation
	title
	citation
	year	



Case name
Volume
Reporter
Frequently cited reporters and abbreviations
Series
Preferred reporters to use as source
1st Page
Pinpoint references
Court
US Courts and abbreviations, abridged listing
Year of decision
Parallel cite
D/M (no vol/pg info)
Weight of authority
Op. Desc (Opinion description)
Court officials abbreviations, abridged listing
Expl. note
ShrtCite ttl (Short Cite case name)
Subsequent history included in citation
Court actions and abbreviations, abridged listing
Hist. Action (Subsequent or prior history, court action
Hist. Cite (Subsequent or prior history citation)
2d Hist. Action
2d Hist. Cite
Note: case name change
Expl. note 2
Case number
Keywords
Access phrase
Abstract
Reference
Cases, unpublished, available in electronic database
Case name
No.
Database year
Database
Identifier
Page
Court
Day/Month
Dec. Year (Decision Year)
Disp. Desc.
Cases, Public Domain (Neutral) Format
Case name
Year
Court
Decision number
Paragraph number
Volume
Reporter
1st Page
Weight of authority
Case, Pending or unreported
Case name
No.
Doc/source
Section/Paragraph
Page
Court
Action
Day/Month
Year
Weight of authority
Hist. action
Hist. cite

http://www.legalcitation.net/qfields.htm
