from zope import component
from zope import interface
from zope.schema.fieldproperty import createFieldProperties
from zope.schema.interfaces import ICollection

from sparc.filter import IExpression
from .filter import SAModelFilterExpression, SAModelFilterExpressionGroup
from . import ISAModelFilterExpressionGroup

@interface.implementer(ISAModelFilterExpressionGroup)
@component.adapter(IExpression)
class SAModelFilterExpressionGroupFromExpression(object):
    createFieldProperties(ISAModelFilterExpressionGroup)
    
    def __init__(self, expression, mapping):
        """
        Args:
            expression: sparc.filter.IExpression provider
            mapping: sparc.filter.IExpression.field to sparc.sa.orm.attributes.ISAInstrumentedAttribute
                     or ISAModelFilterExpression (for fields providing ICollection)
        """
        #recurse value to make sure were dealing in scalars
        value = expression.value
        if IExpression.providedBy(value):
            value = SAModelFilterExpressionGroupFromExpression(value)
        
        #We need an sa expression for each entry in field
        field_entries = expression.field
        if not ICollection.providedBy(expression.field):
            field_entries = [expression.field]
        sa_eg = SAModelFilterExpressionGroup(conjunction=expression.conjunction,
                                             expressions=set([]))
        for field in field_entries:
            sa_eg.expressions.add(SAModelFilterExpression(
                        attribute=mapping[expression.field],
                        condition=expression.condition,
                        value=value
                        ))