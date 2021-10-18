    def compress_p450_conc_gaps(values):
        """ Renames concentrations so they are always %INHIB0-7 rather
            than 0 & 2-7 which can happen in 6 conc results. Also includes
            the concs in each result as CONC0-CONC7"""

        # This function is just for P016 results (but not P016N)
        # P016N does not output %INHIBn values, so don't continue if one is found
        conc_set_name = 'CONC_SET'
        if (not values) or (conc_set_name not in values) or ('%INHIB1' not in values):
            return

        conc_set_string = values[conc_set_name]['unformattedValue']
        conc_set = conc_set_string.split(';')
        included_set = values['INCLUDED_SET']['unformattedValue'].split(';')

        # Reproduce CONC_SET and INCLUDED_SET
        conc_set_values = ['']
        included_set_values = ['']
        for conc, inc in zip(conc_set, included_set):
            if conc != '':
                conc_set_values.append(conc)
                included_set_values.append(inc)
        conc_set_values.append('')
        included_set_values.append('')
        conc_set_str = ';'.join(conc_set_values)
        included_set_str = ';'.join(included_set_values)
        values[conc_set_name]['value'] = values[conc_set_name]['unformattedValue'] = conc_set_str
        values['INCLUDED_SET']['unformattedValue'] = included_set_str
        values['INCLUDED_SET']['value'] = included_set_str

        # Get the headings and values and filter out any blank ones
        conc_values = [values.get('%INHIB{0}'.format(i)) for i in range(8)]
        joined = zip(conc_set[1:-1], conc_values)
        joined = filter(lambda x: x[0] != '', joined)

        # If we have 7 concentrations (including 0) then include a dummy
        # 8th so that P085 results won't have a duplicated top conc.
        # (In P085 with 7 concs, they will be 0, 2-7 instead of 0-6
        # which would have resulted in 7 being duplicated if it's
        # not overwritten)
        if len(joined) == 7:
            joined.append(['na', None])

        units = u'\u00b5M'

        blank = dict(unformattedValue='', value='', relation='=', units='')

        for i, (conc, value) in enumerate(joined):
            value_name = '%INHIB{0}'.format(i)
            conc_name = 'CONC{0}'.format(i)

            # Concs that are 'na' are to be skipped
            # so set their heading to None and delete their values
            if conc == 'na':
                values[value_name] = blank
                if conc_name in values:
                    del values[conc_name]
            else:
                values[conc_name] = dict(unformattedValue=conc, value=conc,
                                        relation='=', units=units)
                values[value_name] = value
