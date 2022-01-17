# Clustering review
## Rationale


### Second constraint


## Usage


### Step 1: choose the deck

### Step 2: input the number of days to postpone
A window will ask you how many days of delay you want to
add. Enter the number, and press ok.

The number can be either negative or positive. A negative number
removes days, which is useful if you added too many days.

The interval of each card is also changed, to reflect the change in
due date. See the configuration section below.

## Configuration
The documentation for the configuration file can be found in
[config.md](config.md).


## Internal
This add-on does not change any methods. Of course, it adds actions in
menus.

## TODO
### Adding smaller intervals to cards due later
Let us assume you had spent a week without using Anki. You use this
add-on and tell Anki so that you don't have to immediately see 7 cards.

But, imagine: maybe even if you don't want to see a full week of
cards in a single day, you'd accept to see 2 days of cards. It will
take twice as much time, but in a week, you won't be late anymore.

If you set this option to 2, you'll see two days of card every day
during a week.

In practice, it means that instead of adding 7 days to every single
card, it will add 7 days to the cards due 7 days ago. It will add 6
days to the card due 6 and 5 days ago. It will add 4 days to the cards
due 4 and 3 days ago, and so on.

### Reorder in function of priority
This add-on does not take into account which cards are urgent and
which ones can wait. Maybe you took a week of holiday. During those
holidays, you were supposed to see cards which you last saw the week
before the holiday, and some other cards you last saw 6 months
ago. Clearly, the first one is more urgent than the second one.

Using this option, you'll still have the same number of cards to see
today, but you'll see the more urgent one first.

Not that the more urgent one may potentially be the hardest one. If
you use this option, you may have a lot of «see again» in the first
days, instead of having a few of them during the whole week.

## Links, license and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>, Jasonbarc https://github.com/jasonsparc
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/Anki-postpone-reviews
Addon number| [1152543397](https://ankiweb.net/shared/info/1152543397)
