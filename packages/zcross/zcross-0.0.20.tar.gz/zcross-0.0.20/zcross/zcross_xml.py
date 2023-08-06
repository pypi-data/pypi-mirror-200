#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as et
import inflection
import os
import sys
import csv
from zcross import Molecule, Electron

def main():
    parser = argparse.ArgumentParser(description = 'Update ZCross XML fields')
    group_get = parser.add_argument_group('Getters')
    group_set = parser.add_argument_group('Setters')

    xsd      = et.parse('/opt/zcross/share/zcross/zcross.xsd')
    xsd_root = xsd.getroot()

    ns = {'xs':'http://www.w3.org/2001/XMLSchema', 'zc': 'https://zcross.net', '': 'https://zcross.net', }

    tag_map = {}

    def decode_xsd_type(xsd_type):
        
        if xsd_type in ('xs:string'):
            return (str, 'STRING')
        if xsd_type in ('xs:integer','xs:int'):
            return (int, 'INT')
        if xsd_type in ('xs:boolean'):
            return (bool, 'BOOL')
        if xsd_type in ('xs:double', 'xs:decimal'):
            return (float, 'FLOAT')
        if xsd_type in ('xs:dateTime'):
            return (str, 'DATETIME')
        raise ValueError(f'Unable to decode: {xsd_type}')
        
    def decode_zc_type(xsd_root, zc_type):
        
        simple_type_xsd = xsd_root.find("xs:simpleType[@name='{}']".format(zc_type.split(':')[1]), ns)
        if simple_type_xsd is not None:
            restriction_xsd = simple_type_xsd.find("xs:restriction", ns)
            if restriction_xsd is not None:
                
                parser_type, parser_metavar = decode_xsd_type(restriction_xsd.get('base'))
                
                choices = []
                
                for enumaration_xsd in restriction_xsd.findall("xs:enumeration", ns):
                    choices.append(parser_type(enumaration_xsd.get('value')))
                
                return (parser_type, parser_metavar, choices) #TODO
          
        raise ValueError(f'Unable to decode: {zc_type}')


    def parse_xsd_attribute(xsd_root, xsd_attribute, parser, span, parent):
        attr_name = xsd_attribute.get('name')
        attr_type = xsd_attribute.get('type')
        
        parm_name = '-'.join([inflection.dasherize(inflection.underscore(p)) for p in parent + [attr_name]][-span:])
        
        parm_help = 'the {} attribute'.format(inflection.dasherize(inflection.underscore(attr_name)).replace('-',' '))
        
        if (len(parent) > 1):
            parm_help += ' of the {} element'.format(parent[-1])
        
        if attr_type.startswith('zc:'):
            parser_type, parser_metavar, parser_choices = decode_zc_type(xsd_root, attr_type)
            group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, choices = parser_choices,  help='Set ' + parm_help)
            group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
            tag_map[parm_name] = parent + ['@' + attr_name]
        else:
            parser_type, parser_metavar = decode_xsd_type(attr_type)
            group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar,    help='Set ' + parm_help)
            group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
            tag_map[parm_name] = parent + ['@' + attr_name]

    def parse_xsd_element(xsd_root, xsd_element, parser, span, parent):
        
        if xsd_element.get('ref') is not None:
            
            if xsd_element.get('ref').startswith('zc:'):
                child_name = xsd_element.get('ref').split(':')[1]
                xsd_element_new =  xsd_root.find("xs:element[@name='{}']".format(child_name), ns)
                parse_xsd(xsd_root, xsd_element_new, parser, span, parent + [child_name])
                
        elif xsd_element.get('name') is not None:
            
            elem_name = xsd_element.get('name')
            elem_type = xsd_element.get('type')
        
            parm_name = '-'.join([inflection.dasherize(inflection.underscore(p)) for p in parent + [elem_name]][-span:])
            
            parm_help = 'the {} element'.format(parm_name.replace('-',' '))
            
           
            if elem_type.startswith('zc:'):
                parser_type, parser_metavar, parser_choices = decode_zc_type(xsd_root, elem_type)
                group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, choices = parser_choices, help='Set ' + parm_help)
                group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
                tag_map[parm_name] = parent + [elem_name]
            else:
                parser_type, parser_metavar = decode_xsd_type(elem_type)
                group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, help='Set ' + parm_help)
                group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
                tag_map[parm_name] =  parent + [elem_name]
            
    def parse_xsd(xsd_root, xsd_element, parser, span=2, parent=[]):

        if xsd_element.get('name') not in ('reactants', 'products'):
            for xsd_attribute in xsd_element.findall("xs:complexType/xs:attribute", ns):
                parse_xsd_attribute(xsd_root, xsd_attribute, parser, span, parent)
                    
            for xsd_subelement in xsd_element.findall("xs:complexType/xs:sequence/xs:element", ns):
                parse_xsd_element(xsd_root, xsd_subelement, parser, span, parent)
                
            for xsd_subelement in xsd_element.findall("xs:complexType/xs:choice/xs:element", ns):
                parse_xsd_element(xsd_root, xsd_subelement, parser, span + 1, parent)
                    
                   
    parser.add_argument('xml')
    parser.add_argument('database_id', nargs='?')
    parser.add_argument('group_id',    nargs='?')
    parser.add_argument('process_id',  nargs='?')

    xsd_zcross = xsd_root.find("xs:element[@name='zcross']", ns)
    parse_xsd(xsd_root, xsd_zcross, parser)

    group_set.add_argument('--set-reactant-1', metavar='SPECIE' )
    group_set.add_argument('--set-reactant-2', metavar='SPECIE' )
    group_set.add_argument('--set-product-1',  metavar='SPECIE' )
    group_set.add_argument('--set-product-2',  metavar='SPECIE' )
    group_set.add_argument('--set-product-3',  metavar='SPECIE' )
    group_set.add_argument('--set-product-4',  metavar='SPECIE' )
    group_set.add_argument('--set-product-5',  metavar='SPECIE' )
    
    group_set.add_argument('--set-database-reference',  nargs=2)

    group_get.add_argument('--get-reactant-1', action='store_true' )
    group_get.add_argument('--get-reactant-2', action='store_true' )
    group_get.add_argument('--get-product-1',  action='store_true' )
    group_get.add_argument('--get-product-2',  action='store_true' )
    group_get.add_argument('--get-product-3',  action='store_true' )
    group_get.add_argument('--get-product-4',  action='store_true' )
    group_get.add_argument('--get-product-5',  action='store_true' )
    
    group_set.add_argument('--get-database-reference', type=int)
    
    parser.add_argument('--load-data', metavar='CSV')
    parser.add_argument('--save-data', metavar='CSV')
    
    parser.add_argument('--unit-energy', default='eV',  metavar='UNIT')
    parser.add_argument('--unit-cross-section',   default='m^2', metavar='UNIT')

    args = parser.parse_args()

    et.register_namespace('','https://zcross.net')
    et.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    has_get = False
    has_set = False

    for arg, value in vars(args).items():
        if arg.startswith('get_') and value == True:
            has_get = True
        if arg.startswith('set_') and value is not None:
            has_set = True
        
    document = None
    document_root = None

    if os.path.exists(args.xml):
        document      = et.parse(args.xml)
        document_root = document.getroot()
    else:
        if has_get and not has_set:
            print(f'Unable to open file: {args.xml}')
            sys.exit(1)
        else:
            document_root = et.Element('{https://zcross.net}zcross')
            document = et.ElementTree(document_root)

    def generate_xpath(path):

        tokens = []
        
        for p in path:
            if not p.startswith('@'):
                token = 'zc:' + p
                if p == 'database':
                    if args.database_id is not None:
                        token += '[@id=\'{}\']'.format(args.database_id)
                    else:
                        print("ERROR: specity the database id")
                        sys.exit(1)
                        
                if p == 'group':
                    if args.group_id is not None:
                        token += '[@id=\'{}\']'.format(args.group_id)
                    else:
                        print("ERROR: specity the group id")
                        sys.exit(1)
                        
                if p == 'process':
                    if args.process_id is not None:
                        token += '[@id=\'{}\']'.format(args.process_id)
                    else:
                        print("ERROR: specity the process id")
                        sys.exit(1)
                tokens.append(token)
                
        return '/'.join(tokens) if tokens else '.'
        
        
    def create_xpath(document_root, path, database_id, group_id, process_id):
        
        
        for i in range(len(path)):
            if not path[i].startswith('@'):
                subelement =  document_root.find(generate_xpath(path[:i+1]), ns)
                if subelement is None:
                    parelement = document_root.find(generate_xpath(path[:i]), ns) if len(path[:i]) > 0 else document_root
                    newelement = et.SubElement(parelement, '{https://zcross.net}'+path[i])
                    
                    if path[i] == 'database':
                        newelement.set('id', database_id)
                    if path[i] == 'group':
                        newelement.set('id', group_id)
                    if path[i] == 'process':
                        newelement.set('id', process_id)
                        
               

    for arg, value in vars(args).items():
        
        custom_tag_map = {
            'reactant-1': ['database', 'groups', 'group', 'processes', 'process', 'reactants'],
            'reactant-2': ['database', 'groups', 'group', 'processes', 'process', 'reactants'],
            'product-1':  ['database', 'groups', 'group', 'processes', 'process', 'products' ],
            'product-2':  ['database', 'groups', 'group', 'processes', 'process', 'products' ],
            'product-3':  ['database', 'groups', 'group', 'processes', 'process', 'products' ],
            'product-4':  ['database', 'groups', 'group', 'processes', 'process', 'products' ],
            'product-5':  ['database', 'groups', 'group', 'processes', 'process', 'products' ],
        }
        
        
        if arg == 'get_database_reference' and value is not None:
            pass
        elif arg == 'set_database_reference' and value is not None:
            
            create_xpath(document_root, ['database', 'references'], args.database_id, args.group_id, args.process_id)
            
            xpath = generate_xpath(['database', 'references']) 
            element_references =  document_root.find(xpath, ns)
            
            element = element_references.find(generate_xpath(['reference']) + '[@id="{}"]'.format(value[0]), ns)
            
            if element is None:
                element = et.SubElement(element_references, '{https://zcross.net}reference', {'id': str(value[0])})
            
            element.text = value[1]
            
        elif arg.startswith('get_') and arg[4:].replace('_','-') in custom_tag_map  and value == True:
            path  = custom_tag_map[arg[4:].replace('_','-')]
            
            xpath = generate_xpath(path)
            element =  document_root.find(xpath, ns)        
            subelement = element.getchildren()[int(arg[4:].split('_')[-1])-1]
            
            specie = None
            if subelement is not None:
                if subelement.tag == '{https://zcross.net}electron':
                    specie = Electron(subelement)
                elif subelement.tag == '{https://zcross.net}molecule':
                    specie = Molecule(subelement)
                    
            print('{:<25} : {}'.format(arg[4:].replace('_',' '), str(specie)))
                
        elif arg.startswith('set_') and arg[4:].replace('_','-') in custom_tag_map  and value is not None:
            
            path  = custom_tag_map[arg[4:].replace('_','-')]
            
            create_xpath(document_root, path, args.database_id, args.group_id, args.process_id)
            
            xpath = generate_xpath(path)
            element =  document_root.find(xpath, ns)
            
            pos = int(arg[4:].split('_')[-1])-1
              
            while len(element.getchildren()) <= pos:
                et.SubElement(element, '{https://zcross.net}molecule')
                
            subelement = element.getchildren()[pos]
                
            if subelement is not None:
                element.remove(subelement)
                
            if value == 'e':
                element.insert(pos, et.Element('{https://zcross.net}electron'))
            else:
                value = value.strip()
                state=''
                if value.endswith(')'):
                    level = 0
                    for c in reversed(value):
                        if c == '(':
                            level -= 1
                        if level > 0:
                            state = c + state
                        if c == ')':
                            level += 1
                        value = value[:-1]
                        if level == 0:
                           break
                           
                state = state.strip()
                value = value.strip()
                charge = 0
                while value.endswith('^+'):
                    value = value[:-2]
                    charge += 1
                while value.endswith('^-'):
                    value = value[:-2]
                    charge -= 1      
                new_element = et.Element('{https://zcross.net}molecule')
                new_element.text = value

                if charge != 0:
                    new_element.set('charge', str(charge))
                if state != '':
                    new_element.set('state', state)
                
                element.insert(pos, new_element)   
                    
        elif arg.startswith('get_') and value == True:  
            path = tag_map[arg[4:].replace('_','-')]
              
            xpath  = generate_xpath(path)
            xattr  = None if not path[-1].startswith('@') else path[-1][1:]

            element =  document_root.find(xpath, ns)
                   
            if element is not None:
                print('{:<25} : {}'.format(arg[4:].replace('_',' '), (element.text if xattr is None else element.get(xattr)) or '')) 
            else:
                print('{:<25} : '.format(arg[4:].replace('_',' ')))
                
        elif arg.startswith('set_') and value is not None:
            path = tag_map[arg[4:].replace('_','-')]
            
            create_xpath(document_root, path, args.database_id, args.group_id, args.process_id)
                       
            element = document_root.find(generate_xpath(path), ns)
            xattr  = None if not path[-1].startswith('@') else path[-1][1:]
           
            if xattr is None:
               element.text = str(value)
            else:
               element.set(xattr, str(value))
               
        elif arg == 'load_data' and value is not None:
            
            data = []
            with open(value) as csvfile:
                
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)
                
                for row in reader:
                    try:
                        float(row[0])
                        float(row[1])
                    except ValueError:
                        continue
                    
                    if len(row) < 2:
                        continue
                        
                    data.append((float(row[0]),float(row[1])))
            
            path = ['database', 'groups', 'group', 'processes', 'process']
            create_xpath(document_root, path, args.database_id, args.group_id, args.process_id)
            
            process_element = document_root.find(generate_xpath(path), ns)
            data_x_element = process_element.find(generate_xpath(['data_x']), ns)
            data_y_element = process_element.find(generate_xpath(['data_y']), ns)
            data_z_element = process_element.find(generate_xpath(['data_z']), ns)
            size_element   = process_element.find(generate_xpath(['size']), ns)

            if data_x_element is not None:
                data_x_element = process_element.find(generate_xpath(['data_x']), ns)
                process_element.remove(data_x_element)
            if data_y_element is not None:
                process_element.remove(data_y_element)
            if data_z_element is not None:
                process_element.remove(data_z_element)
            if size_element is not None:
                process_element.remove(size_element)
           
            size_element   = et.SubElement(process_element, '{https://zcross.net}size')            
            data_x_element = et.SubElement(process_element, '{https://zcross.net}data_x')
            data_y_element = et.SubElement(process_element, '{https://zcross.net}data_y')
            #data_z_element = et.SubElement(process_element, '{https://zcross.net}data_z')

            data_x_element.text = ' '.join([str(d[0]) for d in data])
            data_y_element.text = ' '.join([str(d[1]) for d in data])
            size_element.text   = str(len(data))
            
            data_x_element.set('type', 'energy')
            data_x_element.set('unit', args.unit_energy)
            
            data_y_element.set('type', 'cross_section')
            data_y_element.set('unit', args.unit_cross_section)
            
    if has_set or args.load_data is not None:
        document.write(args.xml,
            xml_declaration = True,
            encoding = 'utf-8',
            method = 'xml')

if __name__ == "__main__":
    main()
