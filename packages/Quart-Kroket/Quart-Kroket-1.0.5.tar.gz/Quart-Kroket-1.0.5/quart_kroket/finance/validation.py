from typing import Optional

from schwifty import IBAN

RE_IBAN = R'([A-Z]{2}[ \-]?[0-9]{2})(?=(?:[ \-]?[A-Z0-9]){9,30}$)((?:[ \-]?[A-Z0-9]{3,5}){2,7})([ \-]?[A-Z0-9]{1,3})?'
RE_VAT_COUNTRY = {
    'Austria': 'ATU[0-9]{8}',
    'Belgium': 'BE0[0-9]{9}',
    'Bulgaria': 'BG[0-9]{9,10}',
    'Cyprus': 'CY[0-9]{8}L',
    'Czech Republic': 'CZ[0-9]{8,10}',
    'Germany': 'DE[0-9]{9}',
    'Denmark': 'DK[0-9]{8}',
    'Estonia': 'EE[0-9]{9}',
    'Greece': 'EL|GR[0-9]{9}',
    'Spain': 'ES[0-9A-Z][0-9]{7}[0-9A-Z]',
    'Finland': 'FI[0-9]{8}',
    'France': 'FR[0-9A-Z]{2}[0-9]{9}',
    'United Kingdom': 'GB([0-9]{9}([0-9]{3}|[A-Z]{2}[0-9]{3})',
    'Hungary': 'HU[0-9]{8}',
    'Ireland': 'IE[0-9]S[0-9]{5}L',
    'Italy': 'IT[0-9]{11}',
    'Lithuania': 'LT([0-9]{9}|[0-9]{12})',
    'Luxembourg': 'LU[0-9]{8}',
    'Latvia': 'LV[0-9]{11}',
    'Malta': 'MT[0-9]{8}',
    'Netherlands': 'NL[0-9]{9}B[0-9]{2}',
    'Poland': 'PL[0-9]{10}',
    'Portugal': 'PT[0-9]{9}',
    'Romania': 'RO[0-9]{2,10}',
    'Sweden': 'SE[0-9]{12}',
    'Slovenia': 'SI[0-9]{8}',
    'Slovakia': 'SK[0-9]{10}'
}


def validate_iban(val: str) -> Optional[IBAN]:
    """Returns IBAN if correct
        >>> iban.compact
        'DE89370400440532013000'
        >>> iban.formatted
        'DE89 3704 0044 0532 0130 00'
        >>> iban.country_code
        'DE'
        >>> iban.bank_code
        '37040044'
        >>> iban.account_code
        '0532013000'
        >>> iban.length
        22
    """
    try:
        return IBAN(val)
    except:
        pass
