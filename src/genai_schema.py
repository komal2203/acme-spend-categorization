classify_fn = {
    'name':'classify_invoice_line',
    'description':'Pick UNSPSC code and confidence',
    'parameters':{
        'type':'object',
        'properties':{
            'code':{'type':'string'},
            'confidence':{'type':'number'}
        },
        'required':['code']
    }
}