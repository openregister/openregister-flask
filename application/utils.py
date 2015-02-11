def log_traceback(logger, ex, ex_traceback=None):
    import traceback
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    logger.info(tb_lines)
