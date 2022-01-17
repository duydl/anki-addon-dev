import anki
from anki.tags import TagManager
import time
from aqt import mw
from typing import Any, Callable, List, Optional, Tuple
from anki.latex import render_latex, render_latex_returning_errors
from anki.utils import intTime
from anki.media import MediaManager, media_paths_from_col_path



def render_all_latex_new(
    self, progress_cb: Optional[Callable[[int], bool]] = None
) -> Optional[Tuple[int, str]]:
    """Render any LaTeX that is missing.
    If a progress callback is provided and it returns false, the operation
    will be aborted.
    If an error is encountered, returns (note_id, error_message)
    """
    failcount = 0
    last_progress = time.time()
    checked = 0
    for (nid, mid, flds) in self.col.db.execute(
        "select id, mid, flds from notes where flds like '%[%'"
    ):

        model = self.col.models.get(mid)
        _html, errors = render_latex_returning_errors(
            flds, model, self.col, expand_clozes=True
        )
        if errors:
            failcount += 1
            # return (nid, "\n".join(errors))
            mw.col.tags.bulk_add([nid], "latex-suspended")
            # mw.col.tags.bulk_add([nid], "marked")
            mw.col.tags.setUserFlag(2, [nid])
            # c = mw.col.backend.get_note(nid).cards()[0]
            # mw.col.sched.suspend_cards([c.id])
        if not errors:
            failcount = 0
        if failcount > 5:
            return nid, "Repeated Errors - You should check"
        checked += 1
        elap = time.time() - last_progress
        if elap >= 0.3 and progress_cb is not None:
            last_progress = intTime()
            if not progress_cb(checked):
                return None

    return None

MediaManager.render_all_latex = render_all_latex_new