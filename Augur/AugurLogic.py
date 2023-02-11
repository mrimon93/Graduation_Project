#%%
import calendar


class AugurLogic:

    def __init__(self):
        pass
    
    def return_str(self, *args):
        month = int(args[2].get())
    
        result = 'With wind average of\n{} m/s\nand '.format(args[0].get()) + \
            'average temperature of\n{}°C\n'.format(args[1].get()) + \
                'in the month of\n{},\n'.format(calendar.month_name[month]) + \
                    'the price should be:\nExpensive!' # some str var...

        # Set 'Predict: result'  
        args[3].set(result)

        return result

        