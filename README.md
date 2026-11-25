# Missing data: what do I do?

A Quarto / reveal.js version of the talk *Why and how to handle missing values
in (longitudinal) research*, made to look like the PowerPoint
(`Missing_values_biomedAI.pptx`).

## Layout

```
index.qmd                    the slides and speaker notes
custom.scss                  type, colours and a few layout helpers
images/bg/                   frames, dividers, title and closing backgrounds
                             exported from the PowerPoint
images/slides/pNN.jpg        whole slides exported from the PowerPoint (page NN
                             of the PDF export), used where the deck has a
                             diagram or animation that is not worth rebuilding
images/                      photos from the PowerPoint
_quarto.yml                  project config
.github/workflows/           render + deploy to GitHub Pages on every push
```

There is no executable code, so `quarto render` takes a few seconds and needs
no R packages. Code on the slides is display only.

The previous, R-heavy version is kept as `index_original_backup.qmd` and
`custom_original_backup.scss`; the scripts it used are still in `R/`.

## Building

```sh
quarto preview index.qmd    # live reload while editing
quarto render               # writes _site/
```

## Slide recipes

```markdown
## Title {background-image="images/bg/frame-lavender.jpg"}   # part 1
## Title {background-image="images/bg/frame-mint.jpg"}       # part 2 (add a [..]{.foot} label)
## Title {background-image="images/bg/frame-yellow.jpg"}     # part 3
## {background-image="images/slides/p13.jpg" background-size="contain"}   # a slide from the deck
```

Helpers in `custom.scss`: `.box .box-mint|lav|yellow|coral`, `.pill .pill-mcar|mar|mnar`,
`.cite`, `.small`, and the colour spans `.mint`, `.coral`, `.amber`, `.purple`.

Fonts: Avenir Next (as in the deck, built into macOS), with Nunito Sans from
Google Fonts as the fallback on other machines.

## Presenting

Slides are a fixed 1280 x 720 (16:9, as in the PowerPoint) and scale to fit
the screen, with white margins when the screen has another shape.

`→` / `←` or the arrows (bottom-right) to move, `m` or ☰ (top-right) for the
slide menu, `b` blank chalkboard, `c` draw on the current slide, `del` clear
drawings, `s` speaker view (notes from the deck are included), `f` full screen,
`e` print view for PDF export.

## Collapsible blocks

`_extensions/collapsible/` (enabled with `filters: [collapsible]` in `index.qmd`)
turns a `.acc` div into a click-to-open block. The first heading is the title:

```markdown
::: {.acc}
### **Listwise deletion**: drop the whole row
- shown only when opened
:::
```

Add `.open` to start it opened. Put `.acc-slide .scrollable` on the slide so
it gets the styling and can scroll when several blocks are open.
