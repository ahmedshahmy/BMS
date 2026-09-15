"""Source content for the BMS newsletter.

This file is the single source of truth for the articles. Every issue below
becomes a folder under ``issues/``, every tile becomes a folder inside that
issue folder containing ``photo.jpg``, ``video.mp4`` and ``text.md``.

The ``text`` field is written out to ``text.md`` and inlined into ``issue.js``
(so a tile reads correctly even when the site is opened straight off disk).
Edit this file, re-run ``tools/build.py``, then commit.

Photos and clips are only generated when they are missing, so replacing a
placeholder ``photo.jpg`` with a real photograph is safe -- use
``tools/build.py --force-media`` if you ever want the placeholders back.

Everything below is placeholder copy written to show the shape of an issue.
"""

SITE = {
    "name": "British Muslim Society",
    "short_name": "BMS",
    "tagline": "Newsletter",
    "description": (
        "The newsletter of the British Muslim Society \u2014 news, prayer "
        "timetables, events and updates from our community."
    ),
    "contact_email": "newsletter@britishmuslimsociety.org.uk",
}

# --------------------------------------------------------------------------
# ISSUES  (newest first -- the first entry is treated as the current issue)
# --------------------------------------------------------------------------

ISSUES = [
    {
        "slug": "2025-11-autumn",
        "number": 12,
        "edition": "Autumn 2025",
        "title": "Autumn Newsletter",
        "published": "2025-11-01",
        "date_label": "November 2025",
        "summary": (
            "A new madrasah year begins, the autumn prayer timetable takes "
            "effect, and our winter warmth appeal opens for the coldest "
            "months ahead."
        ),
        "tiles": [
            {
                "slug": "imams-message",
                "title": "Message from the Imam",
                "icon": "\U0001f54c",
                "blurb": "On gratitude, good neighbours and the coming winter.",
                "text": """## On gratitude and good neighbours

Assalamu alaikum wa rahmatullahi wa barakatuh,

As the clocks go back and the evenings draw in, the masjid becomes the warm
heart of our week once again. It has been a privilege to see so many of you
return after the summer, and to welcome the new families who have joined us
from across the borough.

The Prophet \u0635\u0644\u0649 \u0627\u0644\u0644\u0647 \u0639\u0644\u064a\u0647 \u0648\u0633\u0644\u0645 told us that
*"the best of you are those who are best to their neighbours."* This autumn I
would like us to take that seriously as a community, not simply as a private
virtue.

### Three things we are asking of every household

- **Learn a name.** Our street visit team has knocked on more than 400 doors
  this year. Ask the volunteers for the names of the neighbours on either side
  of you and use them.
- **Share a plate.** The community kitchen runs every Friday after Maghrib.
  Bring one dish a month and you will feed a neighbour you have never met.
- **Check in on the elderly.** Forty-two of our members live alone. The
  befriending rota has room for six more volunteers.

May Allah accept our efforts, keep our community united, and make this winter
a gentle one for those who feel it most keenly.

**Imam Abdul-Rahman Siddiqui**  
*Resident Imam, British Muslim Society*
""",
            },
            {
                "slug": "prayer-timetable",
                "title": "Prayer Timetable",
                "icon": "\U0001f552",
                "blurb": "Autumn timetable, Jumu'ah arrangements and clock changes.",
                "text": """## Autumn prayer timetable

The autumn timetable is now in effect. As the days shorten quickly between
October and December, please check the board in the prayer hall or the masjid
website each month rather than relying on a printed card from the summer.

### Key changes this month

- **Fajr** moves later each week; the first jama'ah is now 25 minutes after
  the adhan so that brothers travelling to work can still join.
- **Isha** is now 7:45 pm at the masjid, with a second jama'ah at 9:00 pm on
  Fridays and Saturdays for students and shift workers.
- **Jumu'ah** remains at **1:15 pm** and **2:15 pm**. The second sitting is
  now the busier of the two \u2014 please arrive by 2:00 pm to find a space in
  the main hall. Overflow seating with a live audio link is available in the
  annexe.

### A reminder about the clocks

The clocks go back on **Sunday 26 October**. The timetable printed in the
October leaflet already accounts for this, but please double-check the display
screen if you are unsure. Maghrib in particular shifts a full hour.

### Facilities

| Facility | Location | Notes |
| --- | --- | --- |
| Wudu area | Ground floor, east wing | Closed for cleaning 30 mins after Isha |
| Sisters' prayer hall | First floor | Lift access from the main entrance |
| Children's room | Annexe | Supervised during Jumu'ah |

> If you are new to the masjid, please introduce yourself to one of the
> stewards in the green lanyards \u2014 they will happily show you around.
""",
            },
            {
                "slug": "madrasah",
                "title": "Madrasah & Education",
                "icon": "\U0001f4da",
                "blurb": "New term, new classes and adult Arabic enrolment.",
                "text": """## The new madrasah year begins

Alhamdulillah, we welcomed **184 pupils** back to the madrasah in September,
our largest intake since the society was founded. Classes run Monday to
Thursday, 5:00 pm to 7:00 pm, with a Friday hifdh circle for pupils who have
completed Juz 30.

### What is new this year

- **Two additional classes** for Years 5 and 6, taught by Ustadha Maryam Khan
  and Ustadh Bilal Ahmed.
- **A dedicated girls' class** on Wednesday evenings in the first-floor
  classroom.
- **Arabic for adults** returns on Tuesday evenings, 8:00 pm to 9:15 pm.
  No prior knowledge is assumed.

### Term dates

| Term | Starts | Ends |
| --- | --- | --- |
| Autumn | 8 September | 12 December |
| Half-term break | 27 October | 31 October |
| Spring | 5 January | 27 March |

### How you can help

We are still looking for two parent volunteers to help with the book stall and
one qualified teacher for the adult Arabic class. If you can give two hours a
week, please speak to the madrasah office or email us.

Fees remain **\u00a315 per month** per child, with a family cap of \u00a330 and
a hardship fund available in confidence for any household that needs it. No
child has ever been turned away from this madrasah for financial reasons, and
none ever will be, insha'Allah.
""",
            },
            {
                "slug": "community-news",
                "title": "Community News",
                "icon": "\U0001f4f0",
                "blurb": "Refurbishment update, new parking rules and the book stall.",
                "text": """## Around the community

### Refurbishment reaches the half-way mark

The wudu facility refurbishment is **60% complete**. The new floor drainage
is installed, and the accessible cubicle is now in use. The remaining work \u2014
tiling, new ablution taps and the hand-dryers \u2014 is scheduled to finish
before the end of November. Our thanks to the eleven volunteers who gave up
three Saturdays to strip out the old fittings.

### Parking on Rutland Road

Following complaints from residents, please **do not park on the double yellow
lines** on Rutland Road before Jumu'ah. The council has agreed to keep the
community centre car park open on Fridays from 12:30 pm, which gives us
roughly forty extra spaces. Marshals will be on the gate from 12:45 pm.

### The book stall is back

The second-hand book stall returns to the foyer every Sunday after Dhuhr.
Donations of Islamic books, children's readers and dictionaries are very
welcome. Proceeds \u2014 **\u00a3400 last year** \u2014 go to the madrasah
library fund.

### In brief

- The lost property box will be emptied on 30 November. Anything unclaimed
  goes to the winter shelter.
- The sisters' halaqah has moved to the first-floor classroom to allow for
  more attendees.
- A defibrillator has been installed by the main entrance. Sixteen members
  have completed training; the next session is on 15 November.
""",
            },
            {
                "slug": "events",
                "title": "Events & Activities",
                "icon": "\U0001f4c5",
                "blurb": "Charity dinner, open day and the winter warmth appeal launch.",
                "text": """## What is coming up

### Annual Charity Dinner \u2014 Saturday 22 November

Our biggest fundraising evening of the year returns to the community hall.
Doors open at **6:30 pm** for a 7:00 pm start, with a three-course meal, a
short address from the Imam and an auction of promises. Tickets are **\u00a320**
for adults and **\u00a310** for under-16s, available from the office after
every jama'ah.

### Masjid Open Day \u2014 Sunday 7 December, 11:00 am \u2013 4:00 pm

A chance for neighbours, schools and local groups to visit. There will be
guided tours of the prayer hall, Arabic calligraphy demonstrations, henna,
and food from our community kitchen. **Please volunteer** \u2014 we need
greeters, guides and bakers. Email the office to be added to the rota.

### Winter Warmth Appeal launch \u2014 from 1 November

See the Charity & Zakat tile for full details. The appeal launches with a
collection after Jumu'ah on 1 November and runs to the end of February.

### Regular gatherings

| Event | When | Where |
| --- | --- | --- |
| Community kitchen | Fridays after Maghrib | Annexe |
| Sisters' halaqah | Tuesdays, 11:00 am | First floor |
| Youth halaqah (13\u201318) | Saturdays, 6:30 pm | Annexe |
| New Muslims circle | First Sunday, 2:00 pm | Meeting room |
""",
            },
            {
                "slug": "youth-corner",
                "title": "Youth Corner",
                "icon": "\u26bd",
                "blurb": "Indoor league, mentoring scheme and exam support.",
                "text": """## Youth news

### Indoor football league kicks off

The winter indoor league starts on **9 November** at the leisure centre on
Mill Lane. Eight teams, twelve weeks, \u00a33 per player per week. Ages 13\u201318.
Sign-up sheets are on the noticeboard, and we need two more parent referees.

### Mentoring scheme needs mentors

Our mentoring scheme pairs GCSE and A-level students with professionals from
the community for one hour a month. Twenty-two young people are waiting for a
mentor. If you work in medicine, engineering, law, IT, teaching or the trades
and can spare an hour a month, please get in touch \u2014 it makes an enormous
difference.

### Exam support sessions

Free study sessions run every Saturday from 4:00 pm in the annexe during the
run-up to mock exams, with a quiet room, past papers, and volunteers on hand
for maths and science.

### Youth committee

The youth committee meets on the first Friday of each month after Isha.
Everyone aged 13\u201318 is welcome, and new ideas are always considered \u2014
last year's committee organised the summer camp, the charity football match
and the Eid funfair.
""",
            },
            {
                "slug": "sisters-corner",
                "title": "Sisters' Corner",
                "icon": "\U0001f338",
                "blurb": "New halaqah times, fitness class and a babysitting rota.",
                "text": """## Sisters' corner

### The halaqah has moved \u2014 and grown

The Tuesday morning halaqah now meets in the **first-floor classroom** at
11:00 am, which gives us room for forty instead of eighteen. We are studying
the names and attributes of Allah, one name a week, with plenty of time for
discussion. Tea and something sweet afterwards, always.

### Women-only fitness, Wednesdays 7:30 pm

A new women-only fitness class has started in the community hall. All
abilities, no experience needed, \u00a34 per session. Please bring a mat if
you have one; we have ten spare.

### Babysitting rota

So that more sisters can attend classes and gatherings, we are setting up a
volunteer babysitting rota in the children's room during Tuesday halaqah and
Wednesday fitness. If you would like to help for one session a month \u2014 or
if you need the service \u2014 please add your name to the sheet in the foyer.

### Sisters' social

The next sisters' social is a **bring-and-share brunch** on Saturday 30
November at 10:30 am. No need to book, just come. It is a relaxed morning and
a good place to meet other sisters if you are new to the area.

> "The believing men and believing women are allies of one another."
> \u2014 Surah at-Tawbah 9:71
""",
            },
            {
                "slug": "charity-zakat",
                "title": "Charity & Zakat",
                "icon": "\U0001f49d",
                "blurb": "Winter warmth appeal, food bank figures and zakat clinic dates.",
                "text": """## Winter warmth appeal

From **1 November** to the end of February we are collecting for the winter
warmth appeal. Last year the community raised **\u00a318,400**, which funded
180 winter packs, four hundred hot meals and emergency heating grants for
eleven local households.

### What we need

- **Coats, blankets and sleeping bags** \u2014 clean and in good condition.
  Drop them in the labelled crates in the foyer.
- **Non-perishable food** \u2014 rice, lentils, tinned tomatoes, oil, tea.
- **Money** \u2014 every pound is spent locally. Gift Aid forms are available
  at the office and add 25% at no cost to you.

### Food bank update

The community food bank distributed **1,240 parcels** in the last twelve
months, up 18% on the year before. Sixty volunteers keep it running. Demand
peaks in January, so please keep the crates filled through the winter.

### Zakat clinic

Our zakat clinic runs on the **first and third Sunday** of each month from
1:00 pm to 3:00 pm. Volunteers can help you calculate your zakat, explain the
nisab thresholds and, if you wish, distribute it directly through the
society's verified channels. All conversations are confidential.

### Where your money went last quarter

| Cause | Amount |
| --- | --- |
| Local hardship grants | \u00a34,120 |
| Food bank running costs | \u00a32,300 |
| Winter packs | \u00a31,850 |
| Overseas emergency relief | \u00a33,000 |
""",
            },
            {
                "slug": "health-wellbeing",
                "title": "Health & Wellbeing",
                "icon": "\u2764\ufe0f",
                "blurb": "Flu clinic, blood pressure checks and mental health support.",
                "text": """## Looking after ourselves

### Free flu clinic at the masjid

The NHS mobile vaccination team will be with us on **Sunday 16 November**,
10:00 am to 2:00 pm, in the annexe. The clinic is free and open to everyone
eligible, and the team is experienced at providing a culturally sensitive
service. Walk in, no appointment needed.

### Blood pressure checks

Volunteer nurses run drop-in blood pressure and blood sugar checks after
Jumu'ah on the last Friday of each month. It takes four minutes and it has
already flagged eleven people for follow-up with their GP.

### Mental health and wellbeing

The wellbeing circle meets on the second Sunday of the month at 3:00 pm. It
is a confidential, facilitated space to talk about stress, grief, anxiety and
the pressures of work and family life. Everything shared stays in the room.

If you or someone you know is struggling, please speak to the Imam or any
member of the wellbeing team. Our faith teaches us to seek help, not to
suffer in silence.

### Staying well this winter

- Get the flu jab if you are eligible.
- Keep moving \u2014 even a twenty-minute walk after Maghrib counts.
- Check on elderly neighbours during cold snaps.
- The masjid is a **warm welcome space** this winter: open 10:00 am to
  4:00 pm daily, warm, with tea and company.
""",
            },
        ],
    },
    {
        "slug": "2025-08-summer",
        "number": 11,
        "edition": "Summer 2025",
        "title": "Summer Newsletter",
        "published": "2025-08-01",
        "date_label": "August 2025",
        "summary": (
            "Eid al-Adha, the Hajj report, a record-breaking summer fete and "
            "our young people's camp in the Peak District."
        ),
        "tiles": [
            {
                "slug": "eid-al-adha",
                "title": "Eid al-Adha",
                "icon": "\U0001f54b",
                "blurb": "Three jama'ahs, 900 worshippers and the qurbani total.",
                "text": """## Eid al-Adha 2025

Alhamdulillah, Eid al-Adha this year brought **over 900 worshippers** through
our doors across three jama'ahs, the largest Eid gathering in the society's
history.

### The day in numbers

| | |
| --- | --- |
| Worshippers | 913 |
| Prayers held | 3 (7:00, 8:30, 10:00 am) |
| Qurbani shares arranged | 62 |
| Children at the funfair | 240 |

### Qurbani

Sixty-two shares were arranged through the society, distributing meat to
families locally and to partners overseas in Gaza, Sudan and Bangladesh. The
cost per share was \u00a365; the committee agreed to subsidise eleven shares
for households in hardship, funded from the general welfare fund.

### Thank you

Eid does not happen by itself. Thank you to the forty volunteers who arrived
at 6:00 am to lay out the halls, the sisters' team who ran the children's
activities, the traffic marshals, and everyone who brought food for the
shared breakfast \u2014 there was enough to send plates to the sheltered
housing on Oakfield Road.
""",
            },
            {
                "slug": "hajj-report",
                "title": "Hajj Report",
                "icon": "\U0001f54b",
                "blurb": "Fourteen of our members completed the pilgrimage.",
                "text": """## Fourteen pilgrims return

Fourteen members of the society performed Hajj this year, including three
married couples and, for the first time, two of our youth volunteers who
travelled with a supervised group. All returned safely, alhamdulillah.

### Their reflections

> "The thing nobody tells you is how ordinary everyone is. You are standing
> shoulder to shoulder with a hundred different nationalities and there is no
> rank at all. I have never felt so small or so much a part of something."
> \u2014 Brother Yusuf, first Hajj

> "I prepared for the heat and the walking. I did not prepare for how much I
> would miss the group when it was over."
> \u2014 Sister Aisha, first Hajj

### A Hajj preparation course

Given the interest, we will run a **Hajj and Umrah preparation course** over
four evenings in the autumn, covering the rites, practical logistics, health
and the spiritual dimensions of the journey. Register your interest at the
office; the course is open to anyone intending to travel in the next two
years.

May Allah accept the pilgrimage of all who went, and grant the same
opportunity to those who long for it.
""",
            },
            {
                "slug": "summer-fete",
                "title": "Summer Fete",
                "icon": "\U0001f389",
                "blurb": "A record \u00a37,200 raised on the sunniest day of the year.",
                "text": """## The summer fete raises a record \u00a37,200

The sun stayed out for the whole of the summer fete and so did the community.
We welcomed an estimated **1,100 visitors** to the field behind the community
centre \u2014 our biggest turnout yet.

### What made it work

- **Food from fourteen countries**, cooked by families from across the
  society. The biryani sold out in ninety minutes.
- **The children's zone**, run by the youth committee, with a bouncy castle,
  face painting and a sponge-the-imam stall that raised \u00a3800 on its own.
- **The bazaar**, with 22 stalls from local Muslim businesses.
- **The car boot sale**, which brought in neighbours who had never set foot
  in the masjid before.

### Where the money goes

The \u00a37,200 raised is split between the masjid refurbishment fund
(\u00a34,000), the madrasah library (\u00a31,700) and the youth camp subsidy
(\u00a31,500).

Thank you to the 63 volunteers and the local businesses who donated prizes,
water and ice cream. Planning for next year starts in January \u2014 new
helpers are very welcome.
""",
            },
            {
                "slug": "youth-camp",
                "title": "Youth Summer Camp",
                "icon": "\u26fa",
                "blurb": "Three days in the Peak District for 38 young people.",
                "text": """## Three days in the Peak District

Thirty-eight young people aged 12\u201317 spent three days at a campsite near
Bakewell in July, accompanied by eight adult volunteers and two qualified
first-aiders.

### What they got up to

- A seven-mile hike across the moor (completed by everyone, with only
  moderate complaining)
- Night-time astronomy, made memorable by a clear sky and no light pollution
- A workshop on leadership and teamwork led by two of our older youth
  volunteers
- Fajr in the open air, which several of the young people said was the
  highlight of the trip

### Feedback from the group

> "I came not knowing anybody. By the second night I had about fifteen
> friends. I did not want to go home."
> \u2014 Participant, age 14

### Next year

The camp is heavily subsidised \u2014 families paid \u00a335 towards a real
cost of about \u00a3140 per head, with the difference met by the fete and by
a donation from a member. If you would like to sponsor a place next year,
please contact the youth team.
""",
            },
            {
                "slug": "madrasah-graduation",
                "title": "Madrasah Graduation",
                "icon": "\U0001f393",
                "blurb": "Eleven pupils complete their hifdh of Juz 30.",
                "text": """## Graduation ceremony 2025

Eleven pupils completed their hifdh of **Juz 30** this year, and four
completed the full Qur'an recitation with tajweed certification. The
graduation ceremony was held in the community hall in front of around three
hundred family members and friends.

### The graduates

Each pupil recited a passage they had chosen themselves. The standard this
year was exceptional, and the examiners commented on the confidence of the
younger pupils in particular.

### Prize winners

| Award | Pupil |
| --- | --- |
| Best overall progress | Sumayya H. |
| Best tajweed | Ibrahim A. |
| Most improved | Zakariya M. |
| Service to the madrasah | Hafsa R. |

### Looking ahead

The madrasah grows every year and we need more teaching capacity. If you are
a fluent reader with a good grasp of tajweed and two hours a week to spare,
please speak to the madrasah office. Training and support are provided, and
all teaching is done in pairs.
""",
            },
            {
                "slug": "sports",
                "title": "Sports",
                "icon": "\U0001f3c6",
                "blurb": "Cricket season review and the inter-masjid football cup.",
                "text": """## Summer of sport

### Cricket

The BMS cricket team finished the season **third in the league**, our best
result yet, with six wins, three losses and one washout. Top scorer was
Brother Hamza with 412 runs; bowler of the season was Brother Idris with 19
wickets.

More importantly, the team ran four Sunday morning coaching sessions for
under-12s, with 55 children attending across the summer.

### Football

The inter-masjid five-a-side cup was hosted at Mill Lane in June. Eight
masjids took part and we reached the semi-final, losing narrowly to the
eventual winners. The atmosphere was superb and the trophy will be back in
the borough next year.

### Coming up

Autumn indoor sessions begin in September for ages 13\u201318, and a walking
football group for the over-50s is being considered \u2014 register your
interest at the office if you would like to join.
""",
            },
            {
                "slug": "volunteers",
                "title": "Volunteer Spotlight",
                "icon": "\U0001f91d",
                "blurb": "Meet the people who keep the society running.",
                "text": """## Volunteer spotlight

The society runs on volunteers. This issue we say thank you to three of them.

### Sister Nasreen \u2014 community kitchen

Nasreen has cooked at the Friday community kitchen for nine years, and rarely
misses a week.

> "I started because I had just retired and I was bored. Now I have about
> forty friends I would never otherwise have met. I get far more out of it
> than I put in."

### Brother Tariq \u2014 maintenance

Tariq, a retired electrician, has rewired half the building, fixed the
boiler twice, and is currently leading the wudu refurbishment.

> "If you can hold a screwdriver, you can help. The trick is to turn up."

### Sister Hina \u2014 safeguarding and youth

Hina leads safeguarding for all our youth activities and has trained eleven
other volunteers.

> "It is not glamorous work. But parents need to know that when they leave
> their children with us, nothing matters more to us than their safety."

### Join them

We currently need: two parent volunteers for the madrasah book stall, six
befrienders for elderly members, two referees for the youth league, and a
treasurer's assistant. Two hours a month is genuinely enough.
""",
            },
        ],
    },
    {
        "slug": "2025-03-ramadan",
        "number": 10,
        "edition": "Ramadan 2025",
        "title": "Ramadan Newsletter",
        "published": "2025-03-01",
        "date_label": "March 2025",
        "summary": (
            "Welcoming Ramadan: taraweeh arrangements, the community iftar "
            "rota, zakat guidance and Eid al-Fitr planning."
        ),
        "tiles": [
            {
                "slug": "welcome-ramadan",
                "title": "Welcome Ramadan",
                "icon": "\U0001f319",
                "blurb": "The blessed month arrives \u2014 and the masjid is ready.",
                "text": """## Welcome to Ramadan

Bismillah. The blessed month is upon us once again, and the masjid has been
prepared for it: the halls cleaned and carpeted, the kitchen stocked, the
timetables printed, and the taraweeh rota filled.

### Our intention for this month

This year the committee has chosen a single theme for Ramadan: **the
neighbour**. Every Friday reminder, every children's activity and every iftar
invitation will return to it. Our neighbours \u2014 Muslim and non-Muslim
alike \u2014 see more of us in Ramadan than in any other month. Let them see
patience, generosity and good humour.

### Practical arrangements

- **Suhoor** packs are available from the office for anyone fasting alone.
- The masjid will be open from **one hour before Fajr** through to 11:00 pm.
- The **community kitchen** serves iftar every single evening. Please book
  for the weekends, which fill up quickly.
- **I'tikaf** in the last ten nights is by registration only; twelve places
  are available.

### A du'a for the month

> "O Allah, bless us in Rajab and Sha'ban, and let us reach Ramadan."
""",
            },
            {
                "slug": "taraweeh",
                "title": "Taraweeh & Prayer",
                "icon": "\U0001f54c",
                "blurb": "Eight or twenty rak'ahs, timings and the youth night.",
                "text": """## Taraweeh and the night prayers

Taraweeh begins on the first night of Ramadan after Isha, at approximately
**8:20 pm**, and finishes around 9:45 pm.

### The schedule

| Prayer | Time | Hall |
| --- | --- | --- |
| Isha | 8:20 pm | Main hall |
| Taraweeh (8 rak'ahs) | 8:35 pm | Main hall |
| Taraweeh (20 rak'ahs) | 8:35 pm | Annexe |
| Tahajjud (last 10 nights) | 2:30 am | Main hall |

We offer both eight and twenty rak'ahs, in separate halls, so that everyone
can pray as they are accustomed. The recitation in the main hall completes
one juz each night, finishing the Qur'an on the twenty-ninth night.

### Youth taraweeh night

Every Saturday, the youth committee leads the first four rak'ahs with two of
our older madrasah pupils reciting. It has become one of the highlights of
the month and the main hall is always full.

### Practical notes

- Please **park considerately** \u2014 taraweeh finishes late and residents
  need access to their drives.
- The sisters' hall is open for every prayer, with a live audio and video
  link from the main hall.
- Wheelchair spaces and chairs are available at the front of both halls.
""",
            },
            {
                "slug": "community-iftar",
                "title": "Community Iftar",
                "icon": "\U0001f37d\ufe0f",
                "blurb": "Thirty nights, thirty families, and how to host one.",
                "text": """## The community iftar

For the whole of Ramadan, the community kitchen serves a free iftar every
evening. Last year we served **6,400 meals** across the month. It takes
roughly thirty families and a small army of volunteers to make it happen.

### Hosting a night

If you would like to sponsor an evening, you can do it in three ways:

- **Cook** \u2014 provide the main dish for around 120 people.
- **Contribute** \u2014 \u00a3150 covers the ingredients for a full evening.
- **Serve** \u2014 join the cleaning and serving rota, one evening a week.

The rota is on the noticeboard and is filling fast. Weekend nights go first,
so if you have a preference, sign up early.

### The neighbours' night

On **Friday 21 March** we are holding a special iftar for our non-Muslim
neighbours, with an open invitation delivered to 300 houses on the surrounding
streets. Last year 74 neighbours came. Please make them welcome \u2014 sit
with someone you do not know and answer their questions warmly.

### Menu

| Day | Main |
| --- | --- |
| Monday | Chicken biryani |
| Tuesday | Lamb pilau |
| Wednesday | Daal and vegetable curry |
| Thursday | Chicken curry and rice |
| Friday | Fish curry |
| Saturday | Community pot luck |
| Sunday | Soup, samosas and pakoras |
""",
            },
            {
                "slug": "zakat-sadaqah",
                "title": "Zakat & Sadaqah",
                "icon": "\U0001f4b0",
                "blurb": "Calculating your zakat and where the society distributes it.",
                "text": """## Zakat and sadaqah in Ramadan

The reward for generosity is multiplied in this month, and the society's
zakat fund is the simplest way to make sure your zakat reaches those who need
it locally.

### Do you need to pay zakat?

Zakat is due on wealth above the **nisab** threshold \u2014 roughly the value
of 87.48 grams of gold \u2014 held for a full lunar year. If you are unsure,
our volunteers will help you work it out. Bring a rough list of your savings,
gold, shares and any money owed to you, and a list of your debts.

### Zakat clinic dates

Sundays **9 March** and **23 March**, 1:00 pm to 3:00 pm in the meeting room.
No appointment needed. All conversations are private.

### Where last year's zakat went

| Category | Share |
| --- | --- |
| Local families in hardship | 46% |
| Orphans and widows (overseas) | 22% |
| Emergency relief | 18% |
| Water and sanitation projects | 9% |
| Education and madrasah places | 5% |

### Sadaqah

Zakat is an obligation; sadaqah is open-ended. The fidyah and kaffarah rate
this year is **\u00a35 per day**. If you would like to feed a fasting person
for the month, \u00a3150 covers a full iftar for the community.
""",
            },
            {
                "slug": "childrens-corner",
                "title": "Children's Corner",
                "icon": "\U0001f31f",
                "blurb": "Ramadan calendars, a colouring competition and the fun day.",
                "text": """## Children's corner

Ramadan is a month children remember for the rest of their lives. Here is how
we are making it special for the youngest members of the society.

### Ramadan calendars

Free wall calendars are available in the foyer for every child. Each day has a
good deed to tick off \u2014 help with the washing up, call a grandparent,
share a toy \u2014 alongside the fasting and prayer trackers. Completed
calendars go into a prize draw on Eid.

### Colouring competition

Entries for the Ramadan colouring competition are now open, in three age
groups: under 6, 7\u201310 and 11\u201314. Sheets are at the back of the hall
and prizes will be awarded at the Eid fun day.

### Children's iftar

A shorter children's iftar runs in the annexe every Saturday at 6:15 pm,
with food children actually want to eat, a short story, and a craft activity.
Parents are welcome to stay.

### Family fun day \u2014 Saturday 29 March

Bouncy castle, henna, a treasure hunt, a lantern-making workshop and the
ever-popular sponge the imam. 2:00 pm to 5:00 pm, free entry, bring the
whole family.

### A note for parents

Please do not pressure young children to fast before they are ready. Let them
practise half-days, keep it joyful, and let the masjid be somewhere they want
to be.
""",
            },
            {
                "slug": "new-muslims",
                "title": "New Muslims",
                "icon": "\U0001f331",
                "blurb": "Six shahadahs, a warm welcome and the revert support circle.",
                "text": """## New Muslims and reverts

**Six people took their shahadah** with the society since the last
newsletter. Each one is a gift to our community, and each one needs more than
a certificate and a handshake.

### The support circle

The new Muslims circle meets on the **first Sunday of the month at 2:00 pm**
in the meeting room. It is led by reverts, for reverts \u2014 covering the
practicalities of prayer, fasting and everyday life alongside the bigger
questions of faith, family and identity.

### Buddy scheme

Every new Muslim is offered a buddy: a member of the society who checks in
weekly for the first six months, answers questions without judgement, and
helps navigate everything from halal shopping to telling your family.

We currently need **four more buddies**. Training and materials are provided.
If you have been Muslim for more than two years, you are qualified \u2014 the
only real requirement is patience and warmth.

### Ramadan for a new Muslim

Fasting your first Ramadan can feel daunting. Please speak to the Imam about
any concessions, health concerns or work arrangements, and let us support
you. There is no expectation of perfection, only of sincerity.
""",
            },
            {
                "slug": "eid-preparations",
                "title": "Eid al-Fitr",
                "icon": "\U0001f389",
                "blurb": "Three jama'ahs, zakat al-fitr and the Eid fun day.",
                "text": """## Preparing for Eid al-Fitr

Eid al-Fitr is expected on **Sunday 30 March**, subject to the sighting of the
moon. Confirmation will be announced on the society's website and by text
message to everyone on the mailing list.

### Prayer arrangements

| Jama'ah | Time | Hall |
| --- | --- | --- |
| First | 7:00 am | Main hall |
| Second | 8:30 am | Main hall |
| Third | 10:00 am | Main hall and annexe |

Please arrive early and, if possible, walk. There will be no parking on
Rutland Road and marshals will direct traffic from 6:30 am.

### Zakat al-Fitr

Zakat al-Fitr is **\u00a37 per person** this year and must reach those
entitled to it **before the Eid prayer**. Please pay at the office or online
by the evening of 29 March at the latest. This is a separate obligation from
zakat on wealth.

### Eid fun day

Straight after the third jama'ah: the Eid fun day on the field. Rides, stalls,
food, sports and the children's prize-giving. Free entry; bring a dish for
the shared table if you can.

### Sunan of Eid

- Take a bath and wear your best clothes.
- Eat something before leaving for the prayer.
- Say the takbir on the way.
- Change your route home.
- And forgive somebody. It is the best thing you can do on Eid.
""",
            },
        ],
    },
]
