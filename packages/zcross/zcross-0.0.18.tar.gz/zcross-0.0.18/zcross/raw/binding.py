# zcross/raw/binding.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:626ec537dfcf4e27e1a94ab21ad8ef1c6da8dfdf
# Generated 2022-09-18 14:47:55.458334 by PyXB version 1.2.6 using Python 3.7.3.final.0
# Namespace https://zcross.net

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:bbf8c4f0-3747-11ed-9528-50eb711e81f1')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('https://zcross.net', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# List simple type: {https://zcross.net}ValueList
# superclasses pyxb.binding.datatypes.anySimpleType
class ValueList (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.double."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ValueList')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 156, 2)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.double
ValueList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'ValueList', ValueList)
_module_typeBindings.ValueList = ValueList

# Atomic simple type: {https://zcross.net}TableType
class TableType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TableType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 159, 2)
    _Documentation = None
TableType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=TableType, enum_prefix=None)
TableType.integral = TableType._CF_enumeration.addEnumeration(unicode_value='integral', tag='integral')
TableType.differential = TableType._CF_enumeration.addEnumeration(unicode_value='differential', tag='differential')
TableType._InitializeFacetMap(TableType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'TableType', TableType)
_module_typeBindings.TableType = TableType

# Atomic simple type: {https://zcross.net}CollisionType
class CollisionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'CollisionType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 165, 2)
    _Documentation = None
CollisionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=CollisionType, enum_prefix=None)
CollisionType.total = CollisionType._CF_enumeration.addEnumeration(unicode_value='total', tag='total')
CollisionType.elastic = CollisionType._CF_enumeration.addEnumeration(unicode_value='elastic', tag='elastic')
CollisionType.inelastic = CollisionType._CF_enumeration.addEnumeration(unicode_value='inelastic', tag='inelastic')
CollisionType.superelastic = CollisionType._CF_enumeration.addEnumeration(unicode_value='superelastic', tag='superelastic')
CollisionType._InitializeFacetMap(CollisionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'CollisionType', CollisionType)
_module_typeBindings.CollisionType = CollisionType

# Atomic simple type: {https://zcross.net}InelasticType
class InelasticType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'InelasticType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 173, 2)
    _Documentation = None
InelasticType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=InelasticType, enum_prefix=None)
InelasticType.excitation_ele = InelasticType._CF_enumeration.addEnumeration(unicode_value='excitation_ele', tag='excitation_ele')
InelasticType.excitation_vib = InelasticType._CF_enumeration.addEnumeration(unicode_value='excitation_vib', tag='excitation_vib')
InelasticType.excitation_rot = InelasticType._CF_enumeration.addEnumeration(unicode_value='excitation_rot', tag='excitation_rot')
InelasticType.ionization = InelasticType._CF_enumeration.addEnumeration(unicode_value='ionization', tag='ionization')
InelasticType.attachment = InelasticType._CF_enumeration.addEnumeration(unicode_value='attachment', tag='attachment')
InelasticType.neutral = InelasticType._CF_enumeration.addEnumeration(unicode_value='neutral', tag='neutral')
InelasticType._InitializeFacetMap(InelasticType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'InelasticType', InelasticType)
_module_typeBindings.InelasticType = InelasticType

# Atomic simple type: {https://zcross.net}DirectionType
class DirectionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DirectionType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 183, 2)
    _Documentation = None
DirectionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=DirectionType, enum_prefix=None)
DirectionType.isotropic = DirectionType._CF_enumeration.addEnumeration(unicode_value='isotropic', tag='isotropic')
DirectionType.anisotropic = DirectionType._CF_enumeration.addEnumeration(unicode_value='anisotropic', tag='anisotropic')
DirectionType.backscattering = DirectionType._CF_enumeration.addEnumeration(unicode_value='backscattering', tag='backscattering')
DirectionType._InitializeFacetMap(DirectionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'DirectionType', DirectionType)
_module_typeBindings.DirectionType = DirectionType

# Atomic simple type: {https://zcross.net}SourceType
class SourceType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SourceType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 190, 2)
    _Documentation = None
SourceType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=SourceType, enum_prefix=None)
SourceType.experiment = SourceType._CF_enumeration.addEnumeration(unicode_value='experiment', tag='experiment')
SourceType.theory = SourceType._CF_enumeration.addEnumeration(unicode_value='theory', tag='theory')
SourceType.mixed = SourceType._CF_enumeration.addEnumeration(unicode_value='mixed', tag='mixed')
SourceType._InitializeFacetMap(SourceType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'SourceType', SourceType)
_module_typeBindings.SourceType = SourceType

# Atomic simple type: {https://zcross.net}DataType
class DataType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataType')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 197, 2)
    _Documentation = None
DataType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=DataType, enum_prefix=None)
DataType.angle = DataType._CF_enumeration.addEnumeration(unicode_value='angle', tag='angle')
DataType.energy = DataType._CF_enumeration.addEnumeration(unicode_value='energy', tag='energy')
DataType.cross_section = DataType._CF_enumeration.addEnumeration(unicode_value='cross_section', tag='cross_section')
DataType._InitializeFacetMap(DataType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'DataType', DataType)
_module_typeBindings.DataType = DataType

# Union simple type: {https://zcross.net}ParameterValue
# superclasses pyxb.binding.datatypes.anySimpleType
class ParameterValue (pyxb.binding.basis.STD_union):

    """Simple type that is a union of pyxb.binding.datatypes.boolean, pyxb.binding.datatypes.integer, pyxb.binding.datatypes.decimal, pyxb.binding.datatypes.double."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ParameterValue')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 204, 2)
    _Documentation = None

    _MemberTypes = ( pyxb.binding.datatypes.boolean, pyxb.binding.datatypes.integer, pyxb.binding.datatypes.decimal, pyxb.binding.datatypes.double, )
ParameterValue._CF_pattern = pyxb.binding.facets.CF_pattern()
ParameterValue._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ParameterValue)
ParameterValue._InitializeFacetMap(ParameterValue._CF_pattern,
   ParameterValue._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ParameterValue', ParameterValue)
_module_typeBindings.ParameterValue = ParameterValue

# Complex type {https://zcross.net}ZCross with content type ELEMENT_ONLY
class ZCross (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}ZCross with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ZCross')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 4, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}database uses Python identifier database
    __database = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'database'), 'database', '__httpszcross_net_ZCross_httpszcross_netdatabase', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 11, 2), )

    
    database = property(__database.value, __database.set, None, None)

    
    # Attribute created uses Python identifier created
    __created = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'created'), 'created', '__httpszcross_net_ZCross_created', pyxb.binding.datatypes.string, required=True)
    __created._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 8, 4)
    __created._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 8, 4)
    
    created = property(__created.value, __created.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpszcross_net_ZCross_version', pyxb.binding.datatypes.string, required=True)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 9, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 9, 4)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        __database.name() : __database
    })
    _AttributeMap.update({
        __created.name() : __created,
        __version.name() : __version
    })
_module_typeBindings.ZCross = ZCross
Namespace.addCategoryObject('typeBinding', 'ZCross', ZCross)


# Complex type {https://zcross.net}Database with content type ELEMENT_ONLY
class Database (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Database with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Database')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 12, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpszcross_net_Database_httpszcross_netname', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 14, 6), )

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {https://zcross.net}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpszcross_net_Database_httpszcross_netdescription', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 15, 6), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {https://zcross.net}contact uses Python identifier contact
    __contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'contact'), 'contact', '__httpszcross_net_Database_httpszcross_netcontact', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 16, 6), )

    
    contact = property(__contact.value, __contact.set, None, None)

    
    # Element {https://zcross.net}url uses Python identifier url
    __url = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'url'), 'url', '__httpszcross_net_Database_httpszcross_neturl', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 17, 6), )

    
    url = property(__url.value, __url.set, None, None)

    
    # Element {https://zcross.net}references uses Python identifier references
    __references = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'references'), 'references', '__httpszcross_net_Database_httpszcross_netreferences', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 25, 2), )

    
    references = property(__references.value, __references.set, None, None)

    
    # Element {https://zcross.net}groups uses Python identifier groups
    __groups = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'groups'), 'groups', '__httpszcross_net_Database_httpszcross_netgroups', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 39, 2), )

    
    groups = property(__groups.value, __groups.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpszcross_net_Database_id', pyxb.binding.datatypes.string, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 21, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 21, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpszcross_net_Database_version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 22, 4)
    __version._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 22, 4)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute refs uses Python identifier refs
    __refs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refs'), 'refs', '__httpszcross_net_Database_refs', pyxb.binding.datatypes.string)
    __refs._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 23, 4)
    __refs._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 23, 4)
    
    refs = property(__refs.value, __refs.set, None, None)

    _ElementMap.update({
        __name.name() : __name,
        __description.name() : __description,
        __contact.name() : __contact,
        __url.name() : __url,
        __references.name() : __references,
        __groups.name() : __groups
    })
    _AttributeMap.update({
        __id.name() : __id,
        __version.name() : __version,
        __refs.name() : __refs
    })
_module_typeBindings.Database = Database
Namespace.addCategoryObject('typeBinding', 'Database', Database)


# Complex type {https://zcross.net}References with content type MIXED
class References (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}References with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'References')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 26, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}reference uses Python identifier reference
    __reference = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reference'), 'reference', '__httpszcross_net_References_httpszcross_netreference', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 31, 2), )

    
    reference = property(__reference.value, __reference.set, None, None)

    _ElementMap.update({
        __reference.name() : __reference
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.References = References
Namespace.addCategoryObject('typeBinding', 'References', References)


# Complex type {https://zcross.net}Reference with content type SIMPLE
class Reference (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Reference with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Reference')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 32, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpszcross_net_Reference_id', pyxb.binding.datatypes.int, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 35, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 35, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.Reference = Reference
Namespace.addCategoryObject('typeBinding', 'Reference', Reference)


# Complex type {https://zcross.net}Groups with content type ELEMENT_ONLY
class Groups (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Groups with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Groups')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 40, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}group uses Python identifier group
    __group = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'group'), 'group', '__httpszcross_net_Groups_httpszcross_netgroup', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 45, 2), )

    
    group = property(__group.value, __group.set, None, None)

    _ElementMap.update({
        __group.name() : __group
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Groups = Groups
Namespace.addCategoryObject('typeBinding', 'Groups', Groups)


# Complex type {https://zcross.net}Processes with content type ELEMENT_ONLY
class Processes (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Processes with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Processes')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 58, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}process uses Python identifier process
    __process = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'process'), 'process', '__httpszcross_net_Processes_httpszcross_netprocess', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 63, 2), )

    
    process = property(__process.value, __process.set, None, None)

    _ElementMap.update({
        __process.name() : __process
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Processes = Processes
Namespace.addCategoryObject('typeBinding', 'Processes', Processes)


# Complex type {https://zcross.net}Reactants with content type ELEMENT_ONLY
class Reactants (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Reactants with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Reactants')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 87, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}electron uses Python identifier electron
    __electron = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'electron'), 'electron', '__httpszcross_net_Reactants_httpszcross_netelectron', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 106, 2), )

    
    electron = property(__electron.value, __electron.set, None, None)

    
    # Element {https://zcross.net}molecule uses Python identifier molecule
    __molecule = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'molecule'), 'molecule', '__httpszcross_net_Reactants_httpszcross_netmolecule', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 108, 2), )

    
    molecule = property(__molecule.value, __molecule.set, None, None)

    _ElementMap.update({
        __electron.name() : __electron,
        __molecule.name() : __molecule
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Reactants = Reactants
Namespace.addCategoryObject('typeBinding', 'Reactants', Reactants)


# Complex type {https://zcross.net}Products with content type ELEMENT_ONLY
class Products (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Products with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Products')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 94, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}electron uses Python identifier electron
    __electron = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'electron'), 'electron', '__httpszcross_net_Products_httpszcross_netelectron', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 106, 2), )

    
    electron = property(__electron.value, __electron.set, None, None)

    
    # Element {https://zcross.net}molecule uses Python identifier molecule
    __molecule = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'molecule'), 'molecule', '__httpszcross_net_Products_httpszcross_netmolecule', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 108, 2), )

    
    molecule = property(__molecule.value, __molecule.set, None, None)

    
    # Attribute weight uses Python identifier weight
    __weight = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'weight'), 'weight', '__httpszcross_net_Products_weight', pyxb.binding.datatypes.double)
    __weight._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 99, 4)
    __weight._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 99, 4)
    
    weight = property(__weight.value, __weight.set, None, None)

    _ElementMap.update({
        __electron.name() : __electron,
        __molecule.name() : __molecule
    })
    _AttributeMap.update({
        __weight.name() : __weight
    })
_module_typeBindings.Products = Products
Namespace.addCategoryObject('typeBinding', 'Products', Products)


# Complex type {https://zcross.net}Reactant with content type MIXED
class Reactant (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Reactant with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Reactant')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 102, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'state'), 'state', '__httpszcross_net_Reactant_state', pyxb.binding.datatypes.string)
    __state._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 103, 4)
    __state._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 103, 4)
    
    state = property(__state.value, __state.set, None, None)

    
    # Attribute charge uses Python identifier charge
    __charge = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'charge'), 'charge', '__httpszcross_net_Reactant_charge', pyxb.binding.datatypes.integer)
    __charge._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 104, 4)
    __charge._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 104, 4)
    
    charge = property(__charge.value, __charge.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __state.name() : __state,
        __charge.name() : __charge
    })
_module_typeBindings.Reactant = Reactant
Namespace.addCategoryObject('typeBinding', 'Reactant', Reactant)


# Complex type {https://zcross.net}Electron with content type EMPTY
class Electron (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Electron with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Electron')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 107, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Electron = Electron
Namespace.addCategoryObject('typeBinding', 'Electron', Electron)


# Complex type {https://zcross.net}Molecule with content type MIXED
class Molecule (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Molecule with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Molecule')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 109, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute state uses Python identifier state
    __state = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'state'), 'state', '__httpszcross_net_Molecule_state', pyxb.binding.datatypes.string)
    __state._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 110, 4)
    __state._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 110, 4)
    
    state = property(__state.value, __state.set, None, None)

    
    # Attribute charge uses Python identifier charge
    __charge = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'charge'), 'charge', '__httpszcross_net_Molecule_charge', pyxb.binding.datatypes.integer)
    __charge._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 111, 4)
    __charge._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 111, 4)
    
    charge = property(__charge.value, __charge.set, None, None)

    
    # Attribute isomer uses Python identifier isomer
    __isomer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'isomer'), 'isomer', '__httpszcross_net_Molecule_isomer', pyxb.binding.datatypes.string)
    __isomer._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 112, 4)
    __isomer._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 112, 4)
    
    isomer = property(__isomer.value, __isomer.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __state.name() : __state,
        __charge.name() : __charge,
        __isomer.name() : __isomer
    })
_module_typeBindings.Molecule = Molecule
Namespace.addCategoryObject('typeBinding', 'Molecule', Molecule)


# Complex type {https://zcross.net}Parameters with content type ELEMENT_ONLY
class Parameters (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Parameters with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Parameters')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 115, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}parameter uses Python identifier parameter
    __parameter = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'parameter'), 'parameter', '__httpszcross_net_Parameters_httpszcross_netparameter', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 147, 2), )

    
    parameter = property(__parameter.value, __parameter.set, None, None)

    _ElementMap.update({
        __parameter.name() : __parameter
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Parameters = Parameters
Namespace.addCategoryObject('typeBinding', 'Parameters', Parameters)


# Complex type {https://zcross.net}Group with content type ELEMENT_ONLY
class Group (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Group with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Group')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 46, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpszcross_net_Group_httpszcross_netdescription', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 48, 6), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {https://zcross.net}processes uses Python identifier processes
    __processes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'processes'), 'processes', '__httpszcross_net_Group_httpszcross_netprocesses', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 57, 2), )

    
    processes = property(__processes.value, __processes.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpszcross_net_Group_id', pyxb.binding.datatypes.string, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 51, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 51, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'alias'), 'alias', '__httpszcross_net_Group_alias', pyxb.binding.datatypes.string)
    __alias._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 52, 4)
    __alias._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 52, 4)
    
    alias = property(__alias.value, __alias.set, None, None)

    
    # Attribute sourceType uses Python identifier sourceType
    __sourceType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sourceType'), 'sourceType', '__httpszcross_net_Group_sourceType', _module_typeBindings.SourceType, required=True)
    __sourceType._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 53, 4)
    __sourceType._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 53, 4)
    
    sourceType = property(__sourceType.value, __sourceType.set, None, None)

    
    # Attribute sourceMethod uses Python identifier sourceMethod
    __sourceMethod = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sourceMethod'), 'sourceMethod', '__httpszcross_net_Group_sourceMethod', pyxb.binding.datatypes.string)
    __sourceMethod._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 54, 4)
    __sourceMethod._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 54, 4)
    
    sourceMethod = property(__sourceMethod.value, __sourceMethod.set, None, None)

    
    # Attribute refs uses Python identifier refs
    __refs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refs'), 'refs', '__httpszcross_net_Group_refs', pyxb.binding.datatypes.string)
    __refs._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 55, 4)
    __refs._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 55, 4)
    
    refs = property(__refs.value, __refs.set, None, None)

    _ElementMap.update({
        __description.name() : __description,
        __processes.name() : __processes
    })
    _AttributeMap.update({
        __id.name() : __id,
        __alias.name() : __alias,
        __sourceType.name() : __sourceType,
        __sourceMethod.name() : __sourceMethod,
        __refs.name() : __refs
    })
_module_typeBindings.Group = Group
Namespace.addCategoryObject('typeBinding', 'Group', Group)


# Complex type {https://zcross.net}Process with content type ELEMENT_ONLY
class Process (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Process with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Process')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 64, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {https://zcross.net}comment uses Python identifier comment
    __comment = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'comment'), 'comment', '__httpszcross_net_Process_httpszcross_netcomment', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 69, 6), )

    
    comment = property(__comment.value, __comment.set, None, None)

    
    # Element {https://zcross.net}updated uses Python identifier updated
    __updated = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'updated'), 'updated', '__httpszcross_net_Process_httpszcross_netupdated', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 70, 6), )

    
    updated = property(__updated.value, __updated.set, None, None)

    
    # Element {https://zcross.net}size uses Python identifier size
    __size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'size'), 'size', '__httpszcross_net_Process_httpszcross_netsize', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 71, 6), )

    
    size = property(__size.value, __size.set, None, None)

    
    # Element {https://zcross.net}reactants uses Python identifier reactants
    __reactants = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'reactants'), 'reactants', '__httpszcross_net_Process_httpszcross_netreactants', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 86, 2), )

    
    reactants = property(__reactants.value, __reactants.set, None, None)

    
    # Element {https://zcross.net}products uses Python identifier products
    __products = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'products'), 'products', '__httpszcross_net_Process_httpszcross_netproducts', True, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 93, 2), )

    
    products = property(__products.value, __products.set, None, None)

    
    # Element {https://zcross.net}parameters uses Python identifier parameters
    __parameters = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'parameters'), 'parameters', '__httpszcross_net_Process_httpszcross_netparameters', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 114, 2), )

    
    parameters = property(__parameters.value, __parameters.set, None, None)

    
    # Element {https://zcross.net}data_x uses Python identifier data_x
    __data_x = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'data_x'), 'data_x', '__httpszcross_net_Process_httpszcross_netdata_x', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 120, 2), )

    
    data_x = property(__data_x.value, __data_x.set, None, None)

    
    # Element {https://zcross.net}data_y uses Python identifier data_y
    __data_y = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'data_y'), 'data_y', '__httpszcross_net_Process_httpszcross_netdata_y', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 129, 2), )

    
    data_y = property(__data_y.value, __data_y.set, None, None)

    
    # Element {https://zcross.net}data_z uses Python identifier data_z
    __data_z = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'data_z'), 'data_z', '__httpszcross_net_Process_httpszcross_netdata_z', False, pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 138, 2), )

    
    data_z = property(__data_z.value, __data_z.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpszcross_net_Process_id', pyxb.binding.datatypes.int)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 76, 4)
    __id._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 76, 4)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute tableType uses Python identifier tableType
    __tableType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tableType'), 'tableType', '__httpszcross_net_Process_tableType', _module_typeBindings.TableType, required=True)
    __tableType._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 77, 4)
    __tableType._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 77, 4)
    
    tableType = property(__tableType.value, __tableType.set, None, None)

    
    # Attribute collisionType uses Python identifier collisionType
    __collisionType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'collisionType'), 'collisionType', '__httpszcross_net_Process_collisionType', _module_typeBindings.CollisionType, required=True)
    __collisionType._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 78, 4)
    __collisionType._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 78, 4)
    
    collisionType = property(__collisionType.value, __collisionType.set, None, None)

    
    # Attribute inelasticType uses Python identifier inelasticType
    __inelasticType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'inelasticType'), 'inelasticType', '__httpszcross_net_Process_inelasticType', _module_typeBindings.InelasticType)
    __inelasticType._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 79, 4)
    __inelasticType._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 79, 4)
    
    inelasticType = property(__inelasticType.value, __inelasticType.set, None, None)

    
    # Attribute dissociative uses Python identifier dissociative
    __dissociative = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'dissociative'), 'dissociative', '__httpszcross_net_Process_dissociative', pyxb.binding.datatypes.boolean)
    __dissociative._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 80, 4)
    __dissociative._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 80, 4)
    
    dissociative = property(__dissociative.value, __dissociative.set, None, None)

    
    # Attribute directionType uses Python identifier directionType
    __directionType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'directionType'), 'directionType', '__httpszcross_net_Process_directionType', _module_typeBindings.DirectionType)
    __directionType._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 81, 4)
    __directionType._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 81, 4)
    
    directionType = property(__directionType.value, __directionType.set, None, None)

    
    # Attribute momentOrder uses Python identifier momentOrder
    __momentOrder = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'momentOrder'), 'momentOrder', '__httpszcross_net_Process_momentOrder', pyxb.binding.datatypes.integer, required=True)
    __momentOrder._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 82, 4)
    __momentOrder._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 82, 4)
    
    momentOrder = property(__momentOrder.value, __momentOrder.set, None, None)

    
    # Attribute refs uses Python identifier refs
    __refs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'refs'), 'refs', '__httpszcross_net_Process_refs', pyxb.binding.datatypes.string)
    __refs._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 83, 4)
    __refs._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 83, 4)
    
    refs = property(__refs.value, __refs.set, None, None)

    
    # Attribute sourceHash uses Python identifier sourceHash
    __sourceHash = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sourceHash'), 'sourceHash', '__httpszcross_net_Process_sourceHash', pyxb.binding.datatypes.string)
    __sourceHash._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 84, 4)
    __sourceHash._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 84, 4)
    
    sourceHash = property(__sourceHash.value, __sourceHash.set, None, None)

    _ElementMap.update({
        __comment.name() : __comment,
        __updated.name() : __updated,
        __size.name() : __size,
        __reactants.name() : __reactants,
        __products.name() : __products,
        __parameters.name() : __parameters,
        __data_x.name() : __data_x,
        __data_y.name() : __data_y,
        __data_z.name() : __data_z
    })
    _AttributeMap.update({
        __id.name() : __id,
        __tableType.name() : __tableType,
        __collisionType.name() : __collisionType,
        __inelasticType.name() : __inelasticType,
        __dissociative.name() : __dissociative,
        __directionType.name() : __directionType,
        __momentOrder.name() : __momentOrder,
        __refs.name() : __refs,
        __sourceHash.name() : __sourceHash
    })
_module_typeBindings.Process = Process
Namespace.addCategoryObject('typeBinding', 'Process', Process)


# Complex type {https://zcross.net}DataX with content type SIMPLE
class DataX (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}DataX with content type SIMPLE"""
    _TypeDefinition = ValueList
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataX')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 121, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is ValueList
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpszcross_net_DataX_type', _module_typeBindings.DataType, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 124, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 124, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__httpszcross_net_DataX_units', pyxb.binding.datatypes.string, required=True)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 125, 8)
    __units._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 125, 8)
    
    units = property(__units.value, __units.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __units.name() : __units
    })
_module_typeBindings.DataX = DataX
Namespace.addCategoryObject('typeBinding', 'DataX', DataX)


# Complex type {https://zcross.net}DataY with content type SIMPLE
class DataY (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}DataY with content type SIMPLE"""
    _TypeDefinition = ValueList
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataY')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 130, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is ValueList
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpszcross_net_DataY_type', _module_typeBindings.DataType, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 133, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 133, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__httpszcross_net_DataY_units', pyxb.binding.datatypes.string, required=True)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 134, 8)
    __units._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 134, 8)
    
    units = property(__units.value, __units.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __units.name() : __units
    })
_module_typeBindings.DataY = DataY
Namespace.addCategoryObject('typeBinding', 'DataY', DataY)


# Complex type {https://zcross.net}DataZ with content type SIMPLE
class DataZ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}DataZ with content type SIMPLE"""
    _TypeDefinition = ValueList
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'DataZ')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 139, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is ValueList
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpszcross_net_DataZ_type', _module_typeBindings.DataType, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 142, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 142, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__httpszcross_net_DataZ_units', pyxb.binding.datatypes.string, required=True)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 143, 8)
    __units._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 143, 8)
    
    units = property(__units.value, __units.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __units.name() : __units
    })
_module_typeBindings.DataZ = DataZ
Namespace.addCategoryObject('typeBinding', 'DataZ', DataZ)


# Complex type {https://zcross.net}Parameter with content type SIMPLE
class Parameter (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {https://zcross.net}Parameter with content type SIMPLE"""
    _TypeDefinition = ParameterValue
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Parameter')
    _XSDLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 148, 2)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is ParameterValue
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpszcross_net_Parameter_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 151, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 151, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__httpszcross_net_Parameter_units', pyxb.binding.datatypes.string)
    __units._DeclarationLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 152, 8)
    __units._UseLocation = pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 152, 8)
    
    units = property(__units.value, __units.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __units.name() : __units
    })
_module_typeBindings.Parameter = Parameter
Namespace.addCategoryObject('typeBinding', 'Parameter', Parameter)


zcross = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'zcross'), ZCross, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 3, 2))
Namespace.addCategoryObject('elementBinding', zcross.name().localName(), zcross)

database = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'database'), Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 11, 2))
Namespace.addCategoryObject('elementBinding', database.name().localName(), database)

references = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'references'), References, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 25, 2))
Namespace.addCategoryObject('elementBinding', references.name().localName(), references)

reference = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), Reference, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 31, 2))
Namespace.addCategoryObject('elementBinding', reference.name().localName(), reference)

groups = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groups'), Groups, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 39, 2))
Namespace.addCategoryObject('elementBinding', groups.name().localName(), groups)

processes = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'processes'), Processes, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 57, 2))
Namespace.addCategoryObject('elementBinding', processes.name().localName(), processes)

reactants = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reactants'), Reactants, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 86, 2))
Namespace.addCategoryObject('elementBinding', reactants.name().localName(), reactants)

products = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'products'), Products, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 93, 2))
Namespace.addCategoryObject('elementBinding', products.name().localName(), products)

reactant = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reactant'), Reactant, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 101, 2))
Namespace.addCategoryObject('elementBinding', reactant.name().localName(), reactant)

electron = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'electron'), Electron, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 106, 2))
Namespace.addCategoryObject('elementBinding', electron.name().localName(), electron)

molecule = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'molecule'), Molecule, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 108, 2))
Namespace.addCategoryObject('elementBinding', molecule.name().localName(), molecule)

parameters = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'parameters'), Parameters, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 114, 2))
Namespace.addCategoryObject('elementBinding', parameters.name().localName(), parameters)

group = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'group'), Group, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 45, 2))
Namespace.addCategoryObject('elementBinding', group.name().localName(), group)

process = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'process'), Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 63, 2))
Namespace.addCategoryObject('elementBinding', process.name().localName(), process)

data_x = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_x'), DataX, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 120, 2))
Namespace.addCategoryObject('elementBinding', data_x.name().localName(), data_x)

data_y = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_y'), DataY, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 129, 2))
Namespace.addCategoryObject('elementBinding', data_y.name().localName(), data_y)

data_z = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_z'), DataZ, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 138, 2))
Namespace.addCategoryObject('elementBinding', data_z.name().localName(), data_z)

parameter = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'parameter'), Parameter, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 147, 2))
Namespace.addCategoryObject('elementBinding', parameter.name().localName(), parameter)



ZCross._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'database'), Database, scope=ZCross, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 11, 2)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ZCross._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'database')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 6, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ZCross._Automaton = _BuildAutomaton()




Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), pyxb.binding.datatypes.string, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 14, 6)))

Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), pyxb.binding.datatypes.string, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 15, 6)))

Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'contact'), pyxb.binding.datatypes.string, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 16, 6)))

Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'url'), pyxb.binding.datatypes.string, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 17, 6)))

Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'references'), References, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 25, 2)))

Database._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'groups'), Groups, scope=Database, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 39, 2)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 16, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 17, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 14, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 15, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'contact')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 16, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'url')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 17, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'references')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 18, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Database._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'groups')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 19, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Database._Automaton = _BuildAutomaton_()




References._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reference'), Reference, scope=References, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 31, 2)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 28, 6))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(References._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reference')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 28, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
References._Automaton = _BuildAutomaton_2()




Groups._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'group'), Group, scope=Groups, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 45, 2)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Groups._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'group')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 42, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Groups._Automaton = _BuildAutomaton_3()




Processes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'process'), Process, scope=Processes, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 63, 2)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Processes._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'process')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 60, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Processes._Automaton = _BuildAutomaton_4()




Reactants._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'electron'), Electron, scope=Reactants, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 106, 2)))

Reactants._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'molecule'), Molecule, scope=Reactants, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 108, 2)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=2, max=2, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 88, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Reactants._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'electron')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 89, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Reactants._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'molecule')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 90, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Reactants._Automaton = _BuildAutomaton_5()




Products._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'electron'), Electron, scope=Products, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 106, 2)))

Products._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'molecule'), Molecule, scope=Products, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 108, 2)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Products._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'electron')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 96, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Products._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'molecule')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 97, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Products._Automaton = _BuildAutomaton_6()




def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
Reactant._Automaton = _BuildAutomaton_7()




def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    return fac.Automaton(states, counters, True, containing_state=None)
Molecule._Automaton = _BuildAutomaton_8()




Parameters._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'parameter'), Parameter, scope=Parameters, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 147, 2)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 116, 4))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Parameters._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'parameter')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 117, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Parameters._Automaton = _BuildAutomaton_9()




Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), pyxb.binding.datatypes.string, scope=Group, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 48, 6)))

Group._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'processes'), Processes, scope=Group, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 57, 2)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 48, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 48, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Group._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'processes')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 49, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Group._Automaton = _BuildAutomaton_10()




Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'comment'), pyxb.binding.datatypes.string, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 69, 6)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'updated'), pyxb.binding.datatypes.dateTime, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 70, 6)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'size'), pyxb.binding.datatypes.integer, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 71, 6)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'reactants'), Reactants, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 86, 2)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'products'), Products, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 93, 2)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'parameters'), Parameters, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 114, 2)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_x'), DataX, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 120, 2)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_y'), DataY, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 129, 2)))

Process._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'data_z'), DataZ, scope=Process, location=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 138, 2)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 67, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 74, 6))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'reactants')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 66, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'products')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 67, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'parameters')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 68, 6))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'comment')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 69, 6))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'updated')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 70, 6))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'size')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 71, 6))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'data_x')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 72, 6))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'data_y')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 73, 6))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Process._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'data_z')), pyxb.utils.utility.Location('/opt/zcross/share/zcross/zcross.xsd', 74, 6))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Process._Automaton = _BuildAutomaton_11()

