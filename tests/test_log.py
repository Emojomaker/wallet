import log


class TestLog():


    def test_type_error(self):
        list_values = [1,'2',(1,2,3),{'4':'5'}, tuple('1')]
        for value in list_values:
            log.log(value)



