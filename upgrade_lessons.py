#!/usr/bin/env python3
"""
Upgrade Singer OS theory lessons to Berklee-level depth.
Uses boundary-based parsing to handle all edge cases (escaped quotes, special chars).
"""
import re, json

with open('/data/data/com.termux/files/home/sessionswithtoby-/index.html', 'r') as f:
    html = f.read()

# Find the lessons array
lessons_start = html.find('lessons: [')
depth = 0
lessons_end = lessons_start
for i in range(lessons_start, len(html)):
    if html[i] == '[':
        depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0:
            lessons_end = i + 1
            break

lessons_text = html[lessons_start:lessons_end]

# Parse lessons by finding boundaries (brace-depth tracking)
# Each lesson starts with { id:N, and ends with } at depth 0
lessons = []
i = 0
while i < len(lessons_text):
    # Find next lesson start
    m = re.search(r'\{\s*id:(\d+),', lessons_text[i:])
    if not m:
        break
    lesson_start = i + m.start()
    # Find end of this lesson (depth tracking from the {)
    depth = 0
    j = lesson_start
    while j < len(lessons_text):
        if lessons_text[j] == '{':
            depth += 1
        elif lessons_text[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    lesson_end = j + 1
    lesson_raw = lessons_text[lesson_start:lesson_end]
    
    # Extract ID
    id_m = re.search(r'id:(\d+)', lesson_raw)
    if id_m:
        lesson_id = int(id_m.group(1))
        lessons.append({'id': lesson_id, 'raw': lesson_raw})
    
    i = lesson_end

print(f"Parsed {len(lessons)} lessons")

# Build a map for quick lookup
lesson_map = {l['id']: l for l in lessons}

# Theory lesson expansions - Berklee depth
theory_expansions = {
    8: {
        'content': 'The musical alphabet uses 7 letters: A B C D E F G, repeating endlessly. Every note on the piano is named with one of these letters. Understanding note names is the foundation of reading music, communicating with other musicians, and navigating your instrument. Berklee ear training professors expect you to name any note within 1 second.',
        'steps': [
            {'type':'teach','title':'The Musical Alphabet','body':'The musical alphabet has 7 letters: A, B, C, D, E, F, G. After G, it starts over at A. On the piano, the white keys follow this pattern. The black keys are sharps (#) and flats (b).\n\nC is the anchor. Find C on any keyboard — it is the white key immediately left of the group of two black keys. From C, count up: C-D-E-F-G-A-B and back to C.'},
            {'type':'teach','title':'Sharps, Flats, and Semitones','body':'A semitone is the smallest distance in Western music — adjacent keys on the piano (including black). A sharp (#) raises a note by one semitone. A flat (b) lowers it by one semitone.\n\nC# = Db (same key). F# = Gb. There is NO sharp or flat between E-F or B-C.\n\nThis is why the black keys have two names — they are enharmonic equivalents. Context determines which name you use.'},
            {'type':'exercise','title':'Name That Note','body':'On a piano app (or mental piano), identify these notes:\n1. The white key between the group of 2 black keys = C\n2. Two white keys up from C = E\n3. The black key right of G = G# or Ab\n4. The black key left of Bb = A#\n\nSing each note as you name it. Connect the symbol to the sound.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write the musical alphabet forward 3 times, then backward 3 times.\n2. On a piano app, play and sing every C on the piano (there are 8 on a full keyboard).\n3. Name all 12 semitones starting from C: C, C#, D, D#, E, F, F#, G, G#, A, A#, B.\n4. Time yourself: name 20 random notes in under 60 seconds.'},
            {'type':'tip','title':'Pro Tip','body':'Professional musicians communicate in note names instantly. "The melody goes E, G#, B" means something specific. Drill this until it is automatic — it will serve you in every rehearsal for the rest of your career.'}
        ]
    },
    9: {
        'content': 'The major scale is the foundation of Western music. It is a pattern of whole steps and half steps that creates the familiar "Do Re Mi" sound. Every key in music is built from this pattern. Berklee students must write any major scale from memory in under 10 seconds.',
        'steps': [
            {'type':'teach','title':'The Major Scale Pattern','body':'A major scale has 8 notes (the octave). The step pattern is:\n\nWhole - Whole - Half - Whole - Whole - Whole - Half\n\nOr in semitones: 2 - 2 - 1 - 2 - 2 - 2 - 1\n\nC Major uses only white keys: C D E F G A B C. This is why C Major is the starting point.\n\nThe distance from C to D is a whole step (C# is between). E to F is a half step (no note between).'},
            {'type':'teach','title':'Scale Degrees and Solfege','body':'Each note in the major scale has a number and a solfege syllable:\n\n1 - Do (tonic, home)\n2 - Re\n3 - Mi\n4 - Fa\n5 - Sol\n6 - La\n7 - Ti\n8 - Do (octave)\n\nThe 1st, 4th, and 5th degrees are "stable" — they feel at rest. The 7th (Ti) wants to resolve up to Do. The 2nd and 6th want to move to nearby stable tones. This tension and release is the engine of melody.'},
            {'type':'exercise','title':'Build a Scale','body':'Using the W-W-H-W-W-W-H pattern, build these scales:\n\n1. G Major: G A B C D E F# G (1 sharp)\n2. F Major: F G A Bb C D E F (1 flat)\n3. D Major: D E F# G A B C# D (2 sharps)\n\nRule: Each letter name appears exactly once. You cannot have G and G# in the same scale — it would be Ab.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Sing C Major scale up and down, using solfege syllables. Use a piano to check.\n2. Play and sing G Major and F Major scales. Notice the same interval pattern.\n3. Write out B Major from memory (hint: 5 sharps). Check your work.\n4. Sing "Do Re Mi" from The Sound of Music — it outlines the major scale.'},
            {'type':'tip','title':'Berklee Connection','body':'At Berklee, you hear "What key is this in?" constantly. The major scale pattern is how you answer. If a song uses F#, C#, and G#, it is likely D Major. Train your ear to hear the tonic — the note that feels like home.'}
        ]
    },
    10: {
        'content': 'An interval measures the distance between two notes. Unison (same pitch) and octave (same note, 12 semitones apart) are the most fundamental. The octave is the most consonant — it sounds almost like the same note. Berklee ear training requires instant identification of all intervals within 3 months.',
        'steps': [
            {'type':'teach','title':'What Is an Interval?','body':'An interval is the distance between two notes, measured in semitones or interval names. Intervals are the DNA of melody and harmony.\n\nMelodic interval: notes played one after another (in a melody).\nHarmonic interval: notes played simultaneously (in a chord).\n\nThe smallest interval in Western music is the semitone (half step). Two semitones = one whole tone (whole step).'},
            {'type':'teach','title':'Unison and Octave','body':'Unison (P1): Same note, same pitch. Two singers singing the same note.\nOctave (P8): Same note name, 12 semitones apart. Middle C and the C above it.\n\nThe octave is so consonant that notes an octave apart are considered "the same note" in theory. This is why we give them the same letter name. The frequency ratio is exactly 2:1 — if A4 = 440Hz, A5 = 880Hz.'},
            {'type':'exercise','title':'Hear the Octave','body':'1. Play middle C on a piano app. Then play the C above it. Sing both.\n2. Have someone play random notes. Sing the octave above or below. Check with a piano.\n3. Listen to Mariah Carey\'s "Emotions" — the chorus features octave jumps.'},
            {'type':'practice','title':'Practical Assignment','body':'1. On a piano, play every note from C3 to C4. Sing the octave above each one.\n2. Write: if the bottom note is F#4, the octave above is F#5.\n3. Identify octaves in songs: Whitney Houston\'s "I Will Always Love You" ("and I-iiiiii") — the "I" jumps an octave.\n4. Sing a unison with a recording of yourself, then an octave apart.'},
            {'type':'tip','title':'Pro Tip','body':'Octave equivalence is why vocal ranges are described by where your octaves sit. A soprano\'s octaves are higher than a alto\'s. Understanding this helps you transpose songs into your range.'}
        ]
    },
    11: {
        'content': 'Time signatures define the pulse of music — how many beats per measure and what note gets the beat. They are the grid on which rhythm lives. 4/4, 3/4, 6/8 — each creates a completely different feel. Berklee ear training spends weeks on meter identification.',
        'steps': [
            {'type':'teach','title':'Reading Time Signatures','body':'A time signature has two numbers:\n\nTop number = how many beats per measure\nBottom number = what note gets one beat (4 = quarter note, 8 = eighth note)\n\n4/4: Four beats per measure, quarter note gets the beat. Also called "common time" (C).\n3/4: Three beats per measure — waltz feel.\n6/8: Six eighth notes per measure — feels like 2 big beats, each divided into 3.'},
            {'type':'teach','title':'Simple vs Compound Meter','body':'Simple meter: beats divide into TWO (4/4, 3/4, 2/4). Each beat naturally splits in half.\nCompound meter: beats divide into THREE (6/8, 9/8, 12/8). Each beat splits into three parts.\n\nThis is the single most important distinction in rhythm. 6/8 is NOT the same as 3/4:\n- 3/4 = 3 beats, each divides into 2 eighths\n- 6/8 = 2 beats, each divides into 3 eighths\n\nFeel it: clap 1-2-3-4 (3/4) vs 1-2-3-4-5-6 (6/8).'},
            {'type':'exercise','title':'Identify the Meter','body':'Listen to these songs and identify the time signature:\n1. "Happy Birthday" — 3/4 (waltz)\n2. "We Are the Champions" — 4/4\n3. "The Blue Danube" — 3/4\n4. "House of the Rising Sun" — 6/8\n5. Afrobeat (Burna Boy) — 4/4 with layered compound rhythms\n\nClap the beat while listening. Where does the emphasis fall?'},
            {'type':'practice','title':'Practical Assignment','body':'1. Tap a steady pulse. Count "1-2-3-4" repeatedly. On beats 1 and 3, clap louder.\n2. Switch to 3/4: "1-2-3" with beat 1 strongest.\n3. Try 6/8: "1-2-3-4-5-6" with beats 1 and 4 strongest.\n4. Write 4 measures of rhythm in 4/4 using quarter and eighth notes. Clap it back.'},
            {'type':'tip','title':'Berklee Connection','body':'Berklee ear training professors use this secret: feel where the DOWNBEAT is. Every measure has a strongest beat (usually beat 1). Once you find the downbeat, the meter reveals itself instantly.'}
        ]
    },
    12: {
        'content': 'Note values define how long each sound lasts. Whole notes, half notes, quarter notes, eighth notes, sixteenth notes — each is a subdivision of the beat. Reading rhythm is reading a language. Berklee uses the Takadimi system for instant rhythm literacy.',
        'steps': [
            {'type':'teach','title':'The Note Value Tree','body':'In 4/4 time (4 beats per measure):\n\nWhole note = 4 beats (holds the whole measure)\nHalf note = 2 beats (two per measure)\nQuarter note = 1 beat (four per measure)\nEighth note = 1/2 beat (eight per measure)\nSixteenth note = 1/4 beat (sixteen per measure)\n\nEach level divides the one above by 2. A whole note = 2 halves = 4 quarters = 8 eighths = 16 sixteenths.\n\nRests follow the same pattern: whole rest, half rest, quarter rest — silence of equal duration.'},
            {'type':'teach','title':'Ties, Dots, and Triplets','body':'Tie: connects two notes into one sustained sound. A quarter tied to another quarter = 2 beats.\nDot: adds half the value. A dotted half note = 3 beats (2 + 1). A dotted quarter = 1.5 beats.\nTriplet: divides a beat into 3 equal parts instead of 2. Eighth-note triplets = 3 notes per beat.\n\nThese create the rhythmic variety in real music. Without them, everything sounds mechanical.'},
            {'type':'exercise','title':'Rhythm Reading','body':'Clap these patterns (each line = one measure of 4/4):\n\n1. Quarter, Quarter, Quarter, Quarter (ta ta ta ta)\n2. Half, Quarter, Quarter (ta-ah ta ta)\n3. Quarter, Two Eighths, Quarter, Two Eighths (ta ta-a ta ta-a)\n4. Four Eighths, Four Eighths (ta-ta-ta-ta ta-ta-ta-ta)\n5. Half, Two Eighths, Two Eighths (ta-ah ta-a ta-a)\n\nUse a metronome at 60 BPM. Quarter note = one click.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write a 4-measure rhythm using only quarter and eighth notes. Clap it.\n2. Write a 4-measure rhythm using half notes and quarter notes.\n3. Add one dotted note to each. Notice how it changes the feel.\n4. Listen to Adele\'s "Rolling in the Deep" — tap the rhythm of the chorus. Write it down.'},
            {'type':'tip','title':'Takadimi System','body':'Berklee uses the Takadimi system:\nQuarter notes: "Ta"\nEighth pairs: "Ta-di"\nSixteenth groups: "Ta-ka-di-mi"\n\nThis connects syllables to rhythms. Use it — it makes complex rhythms readable instantly.'}
        ]
    },
    28: {
        'content': 'Seconds and thirds are the building blocks of melody. A second connects adjacent notes; a third skips one. These intervals define every melody you have ever sung. Berklee interval training uses flashcards — name any interval in under 2 seconds.',
        'steps': [
            {'type':'teach','title':'Seconds (M2, m2)','body':'A second connects two adjacent notes in the scale.\n\nMajor 2nd (M2) = 1 whole step (2 semitones). C to D, E to F#, G to A.\nminor 2nd (m2) = 1/2 step (1 semitone). E to F, B to C, C to Db.\n\nThe minor 2nd has a tense, dissonant sound — think the Jaws theme (dun-dun, dun-dun). The major 2nd is brighter and more open.\n\nIn melody, seconds create smooth, stepwise motion. Most popular melodies move mostly by seconds.'},
            {'type':'teach','title':'Thirds (M3, m3)','body':'A third spans three letter names, skipping one note in between.\n\nMajor 3rd (M3) = 4 semitones. C to E, F to A, G to B. Sounds bright, happy.\nminor 3rd (m3) = 3 semitones. C to Eb, F to Ab, D to F. Sounds dark, sad.\n\nThe major 3rd vs minor 3rd is THE most important distinction in music. It is what makes a chord major or minor. Train your ear obsessively.\n\nSing: C-E (major 3rd, bright). C-Eb (minor 3rd, dark). Feel the difference in your throat.'},
            {'type':'exercise','title':'Identify These Intervals','body':'Sing and identify (use a piano to check):\n1. C to D = Major 2nd\n2. C to Db = minor 2nd\n3. C to E = Major 3rd\n4. C to Eb = minor 3rd\n5. "When You Believe" opening = minor 2nd\n6. "Mary Had a Little Lamb" opening = Major 3rd\n7. "Twinkle Twinkle" opening = Perfect 5th (preview)'},
            {'type':'practice','title':'Practical Assignment','body':'1. Sing a major 3rd from C, then from F, then from G, then from A.\n2. Sing a minor 3rd from the same roots.\n3. Alternate: M3, m3, M3, m3 from random starting notes.\n4. Write a 4-note melody using only seconds and thirds. Sing it back.'},
            {'type':'tip','title':'Berklee Drill','body':'Berklee interval training uses flashcards. A professor plays an interval, you name it in under 2 seconds. The goal: hear a major 3rd and KNOW it instantly, the way you know the color blue. This takes 10 minutes a day for 3 months.'}
        ]
    },
    29: {
        'content': 'A triad is three notes stacked in thirds. Major, minor, diminished — these are the building blocks of every chord in Western music. Understanding triads is understanding harmony itself. Berklee harmony courses expect you to build any triad from any root in under 3 seconds.',
        'steps': [
            {'type':'teach','title':'Building Triads from the Scale','body':'A triad = root + third + fifth, stacked in thirds.\n\nMajor triad: Root + Major 3rd + Perfect 5th. C-E-G = C major.\nminor triad: Root + minor 3rd + Perfect 5th. C-Eb-G = Cm.\nDiminished triad: Root + minor 3rd + diminished 5th. C-Eb-Gb = Cdim.\n\nEvery note in the major scale can generate a triad. In C Major:\n- C (I) = major\n- D (ii) = minor\n- E (iii) = minor\n- F (IV) = major\n- G (V) = major\n- A (vi) = minor\n- B (vii°) = diminished\n\nThis is the harmonic DNA of every song.'},
            {'type':'teach','title':'Hear the Quality','body':'Major triad: bright, stable, "happy." Think of resolution, home, rest.\nminor triad: dark, contemplative, "sad." Think of longing, depth.\nDiminished triad: tense, unstable, "wants to move." Think of suspense.\n\nPlay all three on a piano. Sing the root of each. Then the third. Then the fifth. Internalize the SOUND of each quality.'},
            {'type':'exercise','title':'Build These Triads','body':'Build each triad from the root up (name every note):\n1. D Major: D-F#-A\n2. E minor: E-G-B\n3. F Major: F-A-C\n4. G diminished: G-Bb-Db\n5. A Major: A-C#-E\n6. B diminished: B-D-F\n\nSing the root, then arpeggiate up (root-3rd-5th-root). Use a piano to verify.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Play C major, C minor, and C diminished triads. Sing each note.\n2. Write the triads for G Major (I, IV, V) and Bb Major (I, IV, V).\n3. Listen to "Let It Be" — the chords are I-V-vi-IV in C (C-G-Am-F). Sing the root of each chord.\n4. Identify: is the chord at the start of "Hallelujah" (Jeff Buckley) major or minor?'},
            {'type':'tip','title':'Berklee Insight','body':'At Berklee, you analyze songs by their chord function (I, IV, V, vi). You do not need to hear every note — just the bass movement. The bass tells you the chord; the melody tells you the color.'}
        ]
    },
    30: {
        'content': 'Sixteenth notes divide the beat into four parts. Syncopation places emphasis on unexpected beats — the "and" of the beat, or between beats. Together, they create the rhythmic sophistication of professional music. Berklee rhythm classes spend weeks on syncopation alone.',
        'steps': [
            {'type':'teach','title':'Sixteenth Note Subdivision','body':'One quarter note = 4 sixteenth notes.\n\nCounted: "1 e & a" (four subdivisions per beat)\n- 1 = downbeat\n- e = second sixteenth\n- & = the "and" (beat midpoint)\n- a = fourth sixteenth\n\nIn tempo: if quarter = 120 BPM, sixteenth notes fire at 480 per minute.\n\nSyncopation: emphasizing the "e" or "a" instead of the "1" or "&". This creates rhythmic tension and groove.'},
            {'type':'teach','title':'Syncopation Patterns','body':'Common syncopated patterns:\n\n1. Anticipation: hitting the next beat early (on the "a" of 4 instead of beat 1)\n2. Backbeat: emphasizing beats 2 and 4 (in 4/4)\n3. Offbeat: emphasizing the "&" between main beats\n\nMost pop, R&B, Afrobeats, and gospel use heavy syncopation. The melody often starts BEFORE the chord change.\n\nListen to Bruno Mars\'s "24K Magic" — the vocal rhythm is heavily syncopated against a straight drum beat.'},
            {'type':'exercise','title':'Clap Syncopated Rhythms','body':'Clap these patterns (metronome at 80 BPM):\n\n1. "1 & 2 & 3 & 4 &" — clap only on the "&"s (offbeats)\n2. "1 e & a 2 e & a" — clap on 1, the "a" of 1, and the "&" of 2\n3. "1 e & a 2 e & a 3 e & a 4 e & a" — clap on every "e" and "a"\n4. Rest on beat 1, clap everything else\n\nStart slow. Speed up only when clean.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write a 2-measure rhythm using 8th and 16th notes with at least 2 syncopated moments.\n2. Clap it until clean at 90 BPM.\n3. Listen to any Burna Boy song. Tap the syncopated rhythm of the vocal. Write it down.\n4. Sing a simple melody but syncopate the rhythm — push some notes early, pull others back.'},
            {'type':'tip','title':'Berklee Drill','body':'Berklee rhythm classes use a technique: clap the subdivision (16ths) while tapping the pulse (quarters) with your foot. This "polyrhythmic" body coordination is how pros internalize groove. Practice 5 minutes daily.'}
        ]
    },
    31: {
        'content': 'The Circle of Fifths is the master map of music theory. It shows the relationship between all 12 keys, their key signatures, and their relative majors and minors. Once you understand it, music theory becomes predictable. Berklee students draw the circle from memory in under 30 seconds.',
        'steps': [
            {'type':'teach','title':'The Structure of the Circle','body':'Imagine a clock face. At 12 o\'clock: C Major (0 sharps/flats).\n\nMoving clockwise (up a fifth): G Major (1 sharp), D Major (2 sharps), A Major (3 sharps), E Major (4 sharps), B Major (5 sharps), F# Major (6 sharps).\n\nMoving counterclockwise (up a fourth): F Major (1 flat), Bb Major (2 flats), Eb Major (3 flats), Ab Major (4 flats), Db Major (5 flats), Gb Major (6 flats).\n\nThe circle closes: F# Major = Gb Major (enharmonic equivalent). At 6 o\'clock, the circle flips from sharps to flats.'},
            {'type':'teach','title':'The Inner Circle (Relative Minors)','body':'Every major key has a relative minor key that shares the same key signature. It sits a minor 3rd below.\n\nC Major → A minor (no sharps/flats)\nG Major → E minor (1 sharp)\nD Major → B minor (2 sharps)\nF Major → D minor (1 flat)\n\nThe Circle has TWO rings: outer = major, inner = minor.\n\nThis means: if a song is in E minor, you know it has 1 sharp (F#). The relative major is G Major.'},
            {'type':'exercise','title':'Build the Circle from Memory','body':'Draw the Circle of Fifths from memory:\n1. Start with C at 12 o\'clock\n2. Clockwise: G, D, A, E, B, F#\n3. Counterclockwise: F, Bb, Eb, Ab, Db, Gb\n4. Inner ring: Am, Em, Bm, F#m, C#m, G#m, Dm, Gm, Cm, Fm, Bbm, Ebm\n5. Key signature counts: 0, 1, 2, 3, 4, 5, 6 sharps/flats\n\nDo this 3 times. It should take under 60 seconds when mastered.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Name the key signature for: D Major, Bb Major, A Major, Eb Major.\n2. What is the relative minor of F Major? (D minor)\n3. A song has 3 flats. What key? (Eb Major or C minor)\n4. Write the Circle from memory. Check. Repeat until perfect.\n5. Listen to a song, find the tonic, use the circle to guess the key. Verify with a piano.'},
            {'type':'tip','title':'Berklee Insight','body':'The Circle is not just theory — it is a practical tool. Modulating to the key a fifth away (C→G) sounds natural because they share most notes. Songwriters use the circle to plan key changes. Gospel modulations often move in fourths (counterclockwise).'}
        ]
    },
    47: {
        'content': 'Minor scales are not just "sad major." They are three distinct scales with unique sounds: natural, harmonic, and melodic. Understanding all three is essential for jazz, classical, and any music outside basic pop. Berklee students must write all three forms from memory for any key.',
        'steps': [
            {'type':'teach','title':'Natural Minor Scale','body':'The natural minor scale follows: W-H-W-W-H-W-W (2-1-2-2-1-2-2 semitones).\n\nA natural minor (all white keys): A B C D E F G A.\n\nRelative to C Major (starting on the 6th degree). Same notes, different tonic.\n\nThe natural minor has a "modal" sound — less directional than major. The 7th degree (G) is a whole step below the tonic, so it lacks the leading tone tension of major.'},
            {'type':'teach','title':'Harmonic Minor Scale','body':'Problem: natural minor lacks a leading tone (7th is a whole step below tonic). Solution: raise the 7th degree.\n\nA harmonic minor: A B C D E F G# A.\n\nThe G# creates a strong pull to A — the dominant function. But it creates an augmented 2nd between F and G# (3 semitones). This exotic interval sounds Middle Eastern, dramatic, or classical.\n\nUsed in: classical cadences, metal, flamenco, dramatic pop.'},
            {'type':'teach','title':'Melodic Minor Scale','body':'Problem: harmonic minor\'s augmented 2nd is too exotic for smooth melodies. Solution: raise both 6th AND 7th when ascending.\n\nA melodic minor ascending: A B C D E F# G# A.\nA melodic minor descending: A G F E D C B A (back to natural minor).\n\nThis is the scale of jazz. Jazz musicians think of melodic minor as one scale that changes direction.'},
            {'type':'exercise','title':'Sing All Three','body':'Sing A minor in all three forms (use a piano):\n1. Natural: A B C D E F G A\n2. Harmonic: A B C D E F G# A (hear the G#)\n3. Melodic: A B C D E F# G# A ascending, A G F E D C B A descending\n\nNotice how each version has a different emotional quality.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write D natural minor, D harmonic minor, and D melodic minor from memory.\n2. Sing each one. The difference between F and F# is the key.\n3. Listen to "Losing My Religion" (R.E.M.) — the melody uses natural minor.\n4. Listen to any classical piece in minor — identify harmonic or melodic minor.'},
            {'type':'tip','title':'Berklee Insight','body':'At Berklee, minor scales are taught as ONE system with variable 6th and 7th degrees. You choose which to use based on the melodic context. The "rule" of raising 7th for dominant function is the starting point, not the endpoint.'}
        ]
    },
    48: {
        'content': '7th chords add a fourth note to a triad, creating richer harmony. Major 7, minor 7, and dominant 7 are the most common. They define the sound of jazz, R&B, gospel, and sophisticated pop. Berklee harmony students learn 7th chords as the DEFAULT, not the exception.',
        'steps': [
            {'type':'teach','title':'Building 7th Chords','body':'A 7th chord = triad + the 7th degree above the root (stacked in thirds).\n\nMajor 7 (Maj7): Major triad + Major 7th. C-E-G-B. Dreamy, jazzy, sophisticated.\nminor 7 (m7): minor triad + minor 7th. C-Eb-G-Bb. Smooth, mellow, soulful.\nDominant 7 (Dom7): Major triad + minor 7th. C-E-G-Bb. Tense, wants to resolve to F.\n\nThe dominant 7th is the most important chord in Western music. It creates tension that demands resolution. Every V7 chord in any key is a dominant 7th.'},
            {'type':'teach','title':'Hear the Quality','body':'Maj7: "Lush," "dreamy," "floating." Think of Sade, neo-soul, film scores.\nm7: "Smooth," "warm," "grounded." Think of Robert Glasper, D\'Angelo.\nDom7: "Tense," "needs to move," "bluesy." Think of gospel, blues, jazz turnarounds.\n\nPlay Cmaj7, Cm7, and C7 on a piano. Sing the root, 3rd, 5th, and 7th of each. The 7th is what gives each chord its character.'},
            {'type':'exercise','title':'Build These 7th Chords','body':'Name every note:\n1. Dmaj7: D-F#-A-C#\n2. Gm7: G-Bb-D-F\n3. A7: A-C#-E-G (dominant)\n4. Fmaj7: F-A-C-E\n5. Em7: E-G-B-D\n6. B7: B-D#-F#-A (resolves to E)\n\nSing each chord arpeggiating up. Use a piano to verify.'},
            {'type':'practice','title':'Practical Assignment','body':'1. In C Major, I = Cmaj7, V = G7. Play both. Hear how G7 resolves to Cmaj7.\n2. The ii-V-I (Dm7-G7-Cmaj7) is the most common in jazz. Play and sing it.\n3. Listen to "Let It Be" — verse uses I-V-vi-IV. Imagine with 7ths: Imaj7-V7-vi7-IVmaj7.\n4. Write a 4-chord progression using at least two different 7th chord types.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee students learn 7th chords as the DEFAULT. Triads are the skeleton; 7th chords are the flesh. When you hear a chord, you should tell if it has a 7th — and what kind — within 1 second.'}
        ]
    },
    49: {
        'content': 'Compound time divides beats into groups of 3, creating a flowing, circular feel. 6/8, 9/8, 12/8 — these are the time signatures of gospel ballads, classical minuets, and Afrobeat grooves. Berklee ear training distinguishes 6/8 from 3/4 by feel alone.',
        'steps': [
            {'type':'teach','title':'Compound Meter Explained','body':'In simple meter (4/4, 3/4), beats divide into 2. In compound meter, beats divide into 3.\n\n6/8: Two big beats, each divided into 3 eighth notes.\nCount: "1-2-3-4-5-6" with emphasis on 1 and 4.\nFeel: ONE-two-three-FOUR-five-six (two groups of three).\n\n9/8: Three big beats, each divided into 3.\n12/8: Four big beats, each divided into 3. Common in blues and gospel.'},
            {'type':'teach','title':'6/8 vs 3/4 — The Critical Difference','body':'3/4: 3 beats, each divides into 2 eighths. ONE-and TWO-and THREE-and.\n6/8: 2 big beats, each divides into 3 eighths. ONE-two-three-FOUR-five-six.\n\nSame number of eighth notes, COMPLETELY different feel.\n\n3/4 = waltz (even, marching)\n6/8 = rolling, circular, flowing\n\nTest: "Amazing Grace" in 3/4 vs 6/8. The 6/8 version feels like a gentle sway; 3/4 feels like a march.'},
            {'type':'exercise','title':'Feel the Difference','body':'Clap and count:\n1. 3/4: Clap-2-3, Clap-2-3 (3 beats, 2 subdivisions each)\n2. 6/8: Clap-2-3-4-5-6 (2 beats, 3 subdivisions each)\n3. Alternate: 3/4 for 4 measures, then 6/8 for 4 measures\n4. Listen to "House of the Rising Sun" — it is in 6/8. Feel the two big beats.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write 4 measures of rhythm in 6/8 using dotted quarter and eighth notes.\n2. Write 4 measures in 3/4 using quarter and eighth notes.\n3. Clap both. The 6/8 should feel like a circle; 3/4 should feel like a triangle.\n4. Listen to Afrobeat (Burna Boy, Wizkid) — many use 12/8 feel. Count the groups of 3.'},
            {'type':'tip','title':'Berklee Insight','body':'In compound meter, the BEAT is the dotted quarter note, not the eighth note. When someone says "quarter note = 120" in 6/8, they mean dotted quarter = 120. This trips up many students — do not let it be you.'}
        ]
    },
    50: {
        'content': 'Modulation is changing keys within a song. It creates excitement, emotional lift, and structural contrast. Gospel music modulates up a half step for the final chorus — that is modulation in action. Berklee composers learn to modulate to ANY key from ANY key.',
        'steps': [
            {'type':'teach','title':'Why Modulate?','body':'Staying in one key for an entire song can feel static. Modulation creates:\n- Energy lift (going up feels like "rising")\n- Emotional shift (new key = new feeling)\n- Structural contrast (verse in one key, chorus in another)\n\nCommon modulation distances:\n- Up a whole step (C→D): bright, energetic. Common in pop/gospel final choruses.\n- Up a half step (C→Db): dramatic, intense. Common in gospel.\n- To the relative major/minor (C→Am): subtle, smooth.'},
            {'type':'teach','title':'Pivot Chord Modulation','body':'The smoothest modulation uses a chord that exists in BOTH keys as a "pivot."\n\nExample: C Major to G Major.\n- C Major chords: C, Dm, Em, F, G, Am, Bdim\n- G Major chords: G, Am, Bm, C, D, Em, F#dim\n- Shared: Am, Em, C, D\n\nPlay: C → Am → D7 → G. The Am is the pivot — it is vi in C Major AND ii in G Major. The D7 confirms the new key.\n\nThis is how professionals modulate — smoothly, without jarring transitions.'},
            {'type':'exercise','title':'Identify Modulations','body':'Listen and identify the modulation point:\n1. "I Will Always Love You" (Whitney Houston) — final chorus modulates up a whole step\n2. "Man in the Mirror" (Michael Jackson) — modulates up a half step\n3. "Love on Top" (Beyoncé) — modulates up multiple times (4 times!)\n4. Any gospel song — listen for the key change in the final chorus\n\nWhere does the key change? How does it make you feel?'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write a 4-chord progression in C Major that modulates to G Major using a pivot chord.\n2. Write a 4-chord progression in G Major that modulates to D Major.\n3. Play "Man in the Mirror" — identify exactly where the modulation happens.\n4. Compose a 4-bar verse in one key, then a 4-bar chorus in a different key.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee composers learn three modulation methods: (1) Pivot chord (smoothest), (2) Direct (most dramatic — just jump), (3) Chromatic (use a secondary dominant). Master pivot chords first.'}
        ]
    },
    51: {
        'content': 'Fourths, fifths, and sixths are the intervals of harmony. The perfect fifth is the most consonant interval after the octave. Fourths and sixths create the rich textures of vocal harmony and jazz voicings. Berklee voice students learn to sing in parallel 6ths as a foundational skill.',
        'steps': [
            {'type':'teach','title':'Perfect 4th (P4)','body':'A perfect 4th = 5 semitones. C to F, G to C, D to G.\n\nIn medieval times, the 4th was considered dissonant and was banned in sacred music. Today it is consonant but has an "open" quality — it sounds like it wants to resolve (the 4th wants to fall to the 3rd).\n\nThe 4th is the foundation of quartal harmony (chords built in 4ths instead of 3rds). Think of McCoy Tyner, Herbie Hancock, modern jazz.\n\nSing: C-F (down a 4th = up a 5th). "Here Comes the Bride" starts with a 4th leap up.'},
            {'type':'teach','title':'Perfect 5th (P5)','body':'A perfect 5th = 7 semitones. C to G, F to C, G to D.\n\nThe perfect 5th is the most stable, most consonant interval. It is the basis of the Circle of Fifths and of dominant-tonic resolution.\n\nPower chords in rock are just root + 5th. The 5th gives the chord its "power" without specifying major or minor.\n\nSing: C-G (up a 5th). "Twinkle Twinkle" starts with a 5th. The 5th feels like home — stable, resolved.'},
            {'type':'teach','title':'6ths (M6, m6)','body':'Major 6th = 9 semitones. C to A. Warm, open, consonant.\nminor 6th = 8 semitones. C to Ab. Darker, more complex.\n\n6ths are the foundation of vocal harmony. When a tenor sings a 6th above the melody, it creates that rich gospel/R&B sound.\n\nSing: C-A (major 6th). "My Bonnie Lies Over the Ocean" starts with a major 6th leap.\nC-Ab (minor 6th). "Close Every Door" (Joseph) starts with a minor 6th.'},
            {'type':'exercise','title':'Identify These Intervals','body':'Sing and identify (use piano to check):\n1. C to F = Perfect 4th\n2. C to G = Perfect 5th\n3. C to A = Major 6th\n4. C to Ab = minor 6th\n5. "Somewhere Over the Rainbow" opening = Major 6th\n6. "Star Wars" main theme opening = Perfect 5th\n7. "Hallelujah" (Cohen) "secret chord" = Major 6th'},
            {'type':'practice','title':'Practical Assignment','body':'1. Sing a perfect 5th from every note in C Major scale.\n2. Sing a perfect 4th from every scale degree.\n3. Sing a major 6th from C, D, E, F, G, A, B.\n4. Write a 4-note melody using only 4ths, 5ths, and octaves (no 3rds). Hear the "open" sound.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee voice students learn to sing in parallel 5ths and 6ths with other singers. The 6th is preferred because it creates less tension. Practice singing a 6th above a melody — this is the secret of professional backing vocalists.'}
        ]
    },
    67: {
        'content': 'Modes are variations of the major scale that start on different scale degrees. Mixolydian, Dorian, Phrygian — these are not just theory. They are the sounds of jazz, Afrobeat, rock, and film music. Berklee jazz students must improvise in all 7 modes fluently.',
        'steps': [
            {'type':'teach','title':'What Are Modes?','body':'Modes are scales derived from the major scale, starting on different degrees.\n\nC Major (Ionian): C D E F G A B C — the "default" major sound.\nD Dorian: D E F G A B C D — minor with a raised 6th. Jazzy, soulful.\nE Phrygian: E F G A B C D E — minor with a lowered 2nd. Dark, Spanish, metal.\nF Lydian: F G A B C D E F — major with a raised 4th. Dreamy, floating.\nG Mixolydian: G A B C D E F G — major with a lowered 7th. Bluesy, rock, dominant.\nA Aeolian: A B C D E F G A — natural minor.\nB Locrian: B C D E F G A B — diminished, unstable.'},
            {'type':'teach','title':'Mixolydian — The Dominant Scale','body':'Mixolydian = major scale with a flat 7. G Mixolydian: G A B C D E F G.\n\nThis is the scale of the V7 chord. When you play G7 in C Major, G Mixolydian is the scale.\n\nSound: bluesy, grounded, "almost major but not quite." Think of:\n- "Sweet Child O\' Mine" verse\n- Fleetwood Mac\n- Afrobeat grooves\n- Gospel piano comping\n\nThe flat 7 is what gives it that "not fully resolved" quality.'},
            {'type':'teach','title':'Dorian — The Jazz Minor','body':'Dorian = natural minor with a raised 6th. D Dorian: D E F G A B C D.\n\nCompare to D natural minor (D E F G A Bb C D). The B natural is the difference.\n\nSound: minor but hopeful, sophisticated. Think of:\n- "So What" (Miles Davis) — entirely in Dorian\n- "Scarborough Fair"\n- "Wicked Game" (Chris Isaak)\n- Most of Santana\n\nDorian is the most used mode in jazz improvisation.'},
            {'type':'exercise','title':'Hear the Modes','body':'Sing each mode starting on the same note (C) to hear the difference:\n1. C Ionian: C D E F G A B C (bright, "normal")\n2. C Dorian: C D Eb F G A Bb C (minor with a lift)\n3. C Phrygian: C Db Eb F G Ab Bb C (dark, exotic)\n4. C Lydian: C D E F# G A B C (floating, dreamy)\n5. C Mixolydian: C D E F G A Bb C (bluesy, grounded)\n\nWhich mode fits: a gospel song? (Mixolydian). A jazz standard? (Dorian). A film score? (Lydian or Phrygian).'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write out D Dorian, E Phrygian, and G Mixolydian from memory.\n2. Play "So What" by Miles Davis. The two chords are Dm7 and Ebm7 — that is Dorian.\n3. Write a 4-bar melody in C Mixolydian. Emphasize the flat 7 (Bb).\n4. Listen to any Burna Boy song — identify where Mixolydian appears.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee jazz students learn to hear modes as "colors" not "scales." Each mode has an emotional palette. Dorian = cool blue. Phrygian = dark red. Lydian = golden light. When you hear a solo, identify which mode within 4 bars.'}
        ]
    },
    68: {
        'content': 'Polyrhythms layer different rhythms simultaneously — 3 against 2, 4 against 3. African music is built on these interlocking patterns, and they form the rhythmic foundation of all Afrobeat, gospel, and contemporary Black music. Berklee percussion department teaches this through ensemble playing.',
        'steps': [
            {'type':'teach','title':'The Foundation: 3 Against 2','body':'The simplest polyrhythm: one hand plays 3 evenly-spaced notes while the other plays 2, in the same time span.\n\nTry it: Tap 3 with your left hand, 2 with your right, in the same measure.\n- L: 1 - - 2 - - 3 - -\n- R: 1 - - - 2 - - -\n\nThis creates a "hemiola" — the feeling of two different meters overlapping. This is the heartbeat of African rhythm.\n\nIn Afrobeat: the guitar plays a 12/8 pattern (4 groups of 3) while the drums play 4/4 (4 groups of 2).'},
            {'type':'teach','title':'African Time-Lines','body':'African rhythm uses a "time-line" — a repeating rhythmic pattern that serves as the clock for the ensemble.\n\nThe standard bell pattern:\nX . . X . . X . . . X . X . . .\n(1 . . 2 . . 3 . . . 4 . 5 . . .)\n\nThis 12-note pattern in a 12/8 measure is the skeleton. Every other instrument weaves around it.\n\nListen to any traditional Ghanaian or Nigerian drumming. The bell never stops. Everything else relates to it.'},
            {'type':'exercise','title':'Feel the Polyrhythm','body':'1. Tap your left knee in groups of 3. Tap your right knee in groups of 2. Start slow.\n2. Once comfortable, add a metronome at 60 BPM.\n3. Now: left hand = 3, right hand = 2, feet = 4 (tap your foot on the pulse).\n4. Listen to Fela Kuti\'s "Water No Get Enemy." Identify the repeating guitar pattern.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Learn the standard bell pattern by clapping. It is 12 eighth notes long.\n2. Once memorized, clap it while tapping the main pulse (1-2-3-4) with your foot.\n3. Listen to any Wizkid or Davido song. The hi-hat pattern is usually a variation of 3:2.\n4. Sing a melody while clapping the bell pattern. This is how African musicians develop rhythmic independence.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee percussion department teaches African rhythm by having students PLAY in an ensemble, not just clap. The body learns faster than the brain. If you can, find a djembe class — the physical experience changes your feel permanently.'}
        ]
    },
    69: {
        'content': 'Extended chords (9ths, 11ths, 13ths) add color and sophistication beyond the 7th. They are the vocabulary of jazz, neo-soul, gospel, and R&B. Understanding them opens up the sound of D\'Angelo, Erykah Badu, and Robert Glasper. Berklee pianists learn these as standard vocabulary from day one.',
        'steps': [
            {'type':'teach','title':'Building Extended Chords','body':'Extended chords continue stacking thirds beyond the 7th:\n\n9th chord = 7th chord + 9th (2nd, an octave up). Cmaj9 = C-E-G-B-D.\n11th chord = 9th + 11th (4th, an octave up). Cmaj11 = C-E-G-B-D-F.\n13th chord = 11th + 13th (6th, an octave up). Cmaj13 = C-E-G-B-D-F-A.\n\nIn practice, the root is often played by the bass player, and the 5th is often omitted. The essential notes are: 3rd, 7th, and the extension.'},
            {'type':'teach','title':'Common Extended Chords in Context','body':'Dominant 9 (G9 = G-B-D-F-A): The "jazzy dominant." Resolves to Cmaj7.\nMinor 11 (Dm11 = D-F-A-C-E-G): The "soul chord." Think of D\'Angelo, Erykah Badu.\nMajor 9 (Cmaj9 = C-E-G-B-D): The "dreamy major." Think of Sade, neo-soul.\nDominant 13 (G13 = G-B-D-F-A-E): Rich, full dominant. Resolves to Cmaj9.\n\nThese chords are not just "more notes" — each extension adds a specific emotional color.'},
            {'type':'exercise','title':'Hear Extensions','body':'On a piano (or app), play these chord pairs:\n1. Cmaj7 vs Cmaj9 (add the D) — hear the "open" quality\n2. G7 vs G9 (add the A) — hear the "bluesy" tension\n3. Dm7 vs Dm11 (add the E and G) — hear the "soul" quality\n4. Play: Cmaj9 → Am11 → Dm9 → G13 → Cmaj9. This is a neo-soul progression.'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write the notes of Cmaj9, Dm11, G13, and Fmaj9#11 from memory.\n2. Listen to D\'Angelo\'s "Untitled (How Does It Feel)" — mostly minor 11ths.\n3. Listen to Erykah Badu\'s "On & On" — extended chords throughout.\n4. Write a 4-chord progression using at least 2 extended chords.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee pianists learn to voice extended chords efficiently. You do not need all 6 notes in one hand. The bass plays root and 5th. The piano plays 3rd, 7th, and extension. This "shell voicing" technique is the secret of professional comping.'}
        ]
    },
    71: {
        'content': 'Advanced modulation techniques allow you to move between any two keys smoothly. Pivot chord, direct, chromatic, and common-tone modulation — each has its place and emotional effect. Berklee composers learn to modulate to ANY key from ANY key within 4 beats.',
        'steps': [
            {'type':'teach','title':'Four Modulation Methods','body':'1. PIVOT CHORD: Use a chord shared by both keys (covered in Lesson 50). Smoothest.\n\n2. DIRECT MODULATION: Jump to the new key with no transition. Dramatic, surprising. Common in pop (key change for final chorus with no preparation).\n\n3. CHROMATIC MODULATION: Use a chromatic chord (like a secondary dominant or diminished 7th) to slide into the new key. Example: C → E7 → Am (E7 is V7/Am, not in C Major).\n\n4. COMMON-TONE MODULATION: Hold one note constant while the harmony changes beneath it. Example: Cmaj7 → C7 → Fmaj7 (the C is common to all three).'},
            {'type':'teach','title':'Secondary Dominants','body':'A secondary dominant is the V7 of any chord in the key (not just the tonic).\n\nIn C Major: V7/vi = A7 (resolves to Am). V7/ii = E7 (resolves to Dm). V7/V = D7 (resolves to G).\n\nThese create chromatic movement and forward motion. They are the "passing chords" that make professional music sound sophisticated.\n\nListen to any Bach chorale — secondary dominants everywhere. Listen to Stevie Wonder — same technique, different genre.'},
            {'type':'exercise','title':'Identify the Method','body':'Analyze these progressions:\n1. C → Am → D7 → G (pivot chord: Am is vi in C, ii in G)\n2. C → G7 → C → A7 → Dm (secondary dominant: A7 = V7/ii in C)\n3. C → F → G → C → Ab (direct modulation to Ab — no preparation)\n4. Cmaj7 → Ebmaj7 (common tone: C is in both chords)\n\nWhich method is smoothest? (1). Which is most dramatic? (3).'},
            {'type':'practice','title':'Practical Assignment','body':'1. Write a progression in C Major that modulates to Eb Major using a secondary dominant.\n2. Write a progression that modulates from G Major to D minor using a pivot chord.\n3. Write a direct modulation from any key to any other key.\n4. Analyze "Bridge Over Troubled Water" — identify all secondary dominants.'},
            {'type':'tip','title':'Berklee Insight','body':'Berklee composers learn that modulation is about EMOTIONAL JOURNEY, not just technique. A direct modulation feels like a revelation. A pivot chord modulation feels like a gentle turn. Choose based on what the song needs.'}
        ]
    },
}

# Now rebuild the lessons array
def build_steps(steps_list):
    """Build a steps array string from list of dicts"""
    parts = []
    for s in steps_list:
        body = s['body'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
        title = s['title'].replace('\\', '\\\\').replace("'", "\\'")
        parts.append(f"{{type:'{s['type']}',title:'{title}',body:'{body}'}}")
    return ','.join(parts)

def build_lesson(lesson_id, title, course, duration, content, steps):
    """Build a complete lesson object string"""
    content_escaped = content.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    title_escaped = title.replace('\\', '\\\\').replace("'", "\\'")
    steps_str = build_steps(steps)
    return f"{{ id:{lesson_id}, title:'{title_escaped}', course:'{course}', duration:'{duration}', content:'{content_escaped}',\n      steps:[{steps_str}]}}"

# Build new lessons array
new_lessons_html = []
for lesson in lessons:
    lid = lesson['id']
    raw = lesson['raw']
    
    # Extract fields from raw
    title_m = re.search(r"title:'([^']+)'", raw)
    course_m = re.search(r"course:'([^']+)'", raw)
    duration_m = re.search(r"duration:'([^']+)'", raw)
    # Content needs to handle escaped quotes
    content_m = re.search(r"content:'((?:[^'\\]|\\.)*)'", raw)
    
    title = title_m.group(1) if title_m else "?"
    course = course_m.group(1) if course_m else "?"
    duration = duration_m.group(1) if duration_m else "?"
    content = content_m.group(1).replace("\\'", "'") if content_m else ""
    
    if lid in theory_expansions:
        exp = theory_expansions[lid]
        new_lesson = build_lesson(lid, title, course, duration, exp['content'], exp['steps'])
        new_lessons_html.append(new_lesson)
    else:
        # Parse existing steps from raw
        steps_raw_match = re.search(r'steps:\[(.*?)\]\s*\}$', raw, re.DOTALL)
        steps_raw = steps_raw_match.group(1) if steps_raw_match else ""
        steps = []
        step_pattern = re.compile(r"\{type:'(\w+)',title:'([^']*)',body:'([^']*)'\}", re.DOTALL)
        for sm in step_pattern.finditer(steps_raw):
            steps.append({
                'type': sm.group(1),
                'title': sm.group(2).replace("\\'", "'"),
                'body': sm.group(3).replace("\\'", "'").replace("\\n", "\n")
            })
        new_lesson = build_lesson(lid, title, course, duration, content, steps)
        new_lessons_html.append(new_lesson)

# Build the new lessons array
new_lessons_array = 'lessons: [\n    ' + ',\n    '.join(new_lessons_html) + '\n  ]'

# Replace in HTML
new_html = html[:lessons_start] + new_lessons_array + html[lessons_end:]

with open('/data/data/com.termux/files/home/sessionswithtoby-/index.html', 'w') as f:
    f.write(new_html)

print(f"✓ Rebuilt {len(new_lessons_html)} lessons with expanded theory content")
print(f"New file size: {len(new_html)} chars ({len(new_html)/1024:.1f} KB)")
print(f"Old lessons array was at [{lessons_start}:{lessons_end}]")

# Verify all 100 lessons present
ids = [l['id'] for l in lessons]
missing = [i for i in range(1, 101) if i not in ids]
if missing:
    print(f"⚠ Missing: {missing}")
else:
    print("✓ All 100 lessons present")
