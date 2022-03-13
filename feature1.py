def test_a1(tc):
    tc.logger.info('Inside %s', tc.function.name)
    tc.logger.info('My log dir is %s', tc.log_dir)
    tc.logger.info('My log file is %s', tc.log_file)


def test_a2(tc):
    tc.logger.info('Inside %s', tc.function.name)
    tc.logger.info('My log dir is %s', tc.log_dir)
    tc.logger.info('My log file is %s', tc.log_file)
