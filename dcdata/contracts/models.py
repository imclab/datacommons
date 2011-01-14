from django.contrib.localflavor.us.models import USStateField
from django.db import models
from dcdata.models import Import
from dcdata.contracts import *

class Contract(models.Model):
    imported_on = models.DateField(auto_now_add=True)
    
    unique_transaction_id = models.CharField(max_length=32, blank=True)
    transaction_status = models.CharField(max_length=32, blank=True)
    vendorname = models.CharField(max_length=400, blank=True)
    lastdatetoorder = models.CharField(max_length=32, blank=True)
    agencyid = models.CharField(max_length=4, blank=True)
    account_title = models.CharField(max_length=255, blank=True)
    piid = models.CharField(max_length=50, blank=True)
    modnumber = models.CharField(max_length=25, blank=True)
    vendordoingasbusinessname = models.CharField(max_length=400, blank=True)
    transactionnumber = models.CharField(max_length=6, blank=True)
    idvagencyid = models.CharField(max_length=4, blank=True)
    idvpiid = models.CharField(max_length=50, blank=True)
    aiobflag = models.CharField(max_length=1, blank=True)
    idvmodificationnumber  = models.CharField(max_length=25, blank=True)
    signeddate = models.DateField(blank=True, null=True)
    effectivedate = models.DateField(blank=True, null=True)
    currentcompletiondate = models.DateField(blank=True, null=True)
    ultimatecompletiondate = models.DateField(blank=True, null=True)
    obligatedamount = models.DecimalField(default=0, max_digits=20, decimal_places=2, blank=True, null=True)
    shelteredworkshopflag = models.NullBooleanField()
    baseandexercisedoptionsvalue = models.DecimalField(default=0, max_digits=20, decimal_places=2, blank=True, null=True)
    veteranownedflag = models.NullBooleanField()
    srdvobflag = models.NullBooleanField()
    baseandalloptionsvalue = models.DecimalField(default=0, max_digits=20, decimal_places=2, blank=True, null=True)
    contractingofficeagencyid = models.CharField(max_length=4, blank=True)
    womenownedflag = models.NullBooleanField()
    contractingofficeid = models.CharField(max_length=6, blank=True)
    minorityownedbusinessflag = models.NullBooleanField()
    fundingrequestingagencyid = models.CharField(max_length=4, blank=True)
    saaobflag = models.NullBooleanField()
    apaobflag = models.NullBooleanField()
    fundingrequestingofficeid = models.CharField(max_length=6, blank=True)
    purchasereason = models.CharField(max_length=1, blank=True)
    baobflag = models.NullBooleanField()
    fundedbyforeignentity = models.CharField(max_length=1, blank=True)
    haobflag = models.NullBooleanField()
    naobflag = models.NullBooleanField()
    contractactiontype = models.CharField(max_length=1, blank=True)
    typeofcontractpricing = models.CharField(max_length=1, blank=True)
    verysmallbusinessflag = models.NullBooleanField()
    reasonformodification = models.CharField(max_length=1, blank=True)
    federalgovernmentflag = models.NullBooleanField()
    majorprogramcode = models.CharField(max_length=100, blank=True)
    costorpricingdata = models.CharField(max_length=1, blank=True)
    solicitationid = models.CharField(max_length=25, blank=True)
    costaccountingstandardsclause = models.CharField(max_length=1, blank=True)
    stategovernmentflag = models.NullBooleanField()
    descriptionofcontractrequirement = models.TextField(blank=True)
    localgovernmentflag = models.NullBooleanField()
    gfe_gfp = models.NullBooleanField()
    seatransportation = models.CharField(max_length=1, blank=True)
    consolidatedcontract = models.NullBooleanField()
    lettercontract = models.CharField(max_length=1, blank=True)
    multiyearcontract = models.NullBooleanField()
    performancebasedservicecontract = models.CharField(max_length=1, blank=True)
    contingencyhumanitarianpeacekeepingoperation = models.CharField(max_length=1, blank=True)
    tribalgovernmentflag = models.NullBooleanField()
    contractfinancing = models.CharField(max_length=1, blank=True)
    purchasecardaspaymentmethod = models.NullBooleanField()
    numberofactions = models.IntegerField(null=True)
    walshhealyact = models.NullBooleanField()
    servicecontractact = models.NullBooleanField()
    davisbaconact = models.NullBooleanField()
    clingercohenact = models.NullBooleanField()
    interagencycontractingauthority = models.CharField(max_length=1, blank=True)
    productorservicecode = models.CharField(max_length=4, blank=True)
    contractbundling = models.CharField(max_length=1, blank=True)
    claimantprogramcode = models.CharField(max_length=3, blank=True)
    principalnaicscode = models.CharField(max_length=6, blank=True)
    recoveredmaterialclauses = models.CharField(max_length=1, blank=True)
    educationalinstitutionflag = models.NullBooleanField()
    systemequipmentcode = models.CharField(max_length=4, blank=True)
    hospitalflag = models.NullBooleanField()
    informationtechnologycommercialitemcategory = models.CharField(max_length=1, blank=True)
    useofepadesignatedproducts = models.CharField(max_length=1, blank=True)
    countryoforigin = models.CharField(max_length=2, blank=True)
    placeofmanufacture = models.CharField(max_length=1, blank=True)
    streetaddress = models.CharField(max_length=400, blank=True)
    streetaddress2 = models.CharField(max_length=400, blank=True)
    streetaddress3 = models.CharField(max_length=400, blank=True)
    city = models.CharField(max_length=35, blank=True)
    state = USStateField(blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    vendorcountrycode = models.CharField(max_length=3, blank=True)
    dunsnumber = models.CharField(max_length=13, blank=True)
    congressionaldistrict = models.CharField(max_length=6, blank=True)
    locationcode = models.CharField(max_length=5, blank=True)
    statecode = USStateField(blank=True)
    placeofperformancecountrycode = models.CharField(max_length=3, blank=True)
    placeofperformancezipcode = models.CharField(max_length=10, blank=True)
    nonprofitorganizationflag = models.NullBooleanField()
    placeofperformancecongressionaldistrict = models.CharField(max_length=6, blank=True)
    extentcompeted = models.CharField(max_length=3, blank=True)
    competitiveprocedures = models.CharField(max_length=3, blank=True)
    solicitationprocedures = models.CharField(max_length=5, blank=True)
    typeofsetaside = models.CharField(max_length=10, blank=True)
    organizationaltype = models.CharField(max_length=30, blank=True)
    evaluatedpreference = models.CharField(max_length=6, blank=True)
    numberofemployees = models.IntegerField(null=True)
    research = models.CharField(max_length=3, blank=True)
    annualrevenue = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    statutoryexceptiontofairopportunity = models.CharField(max_length=4, blank=True)
    reasonnotcompeted = models.CharField(max_length=3, blank=True)
    numberofoffersreceived = models.IntegerField(null=True)
    commercialitemacquisitionprocedures = models.CharField(max_length=1, blank=True)
    hbcuflag = models.NullBooleanField()
    commercialitemtestprogram = models.NullBooleanField()
    smallbusinesscompetitivenessdemonstrationprogram = models.CharField(max_length=1, blank=True)
    a76action = models.NullBooleanField()
    sdbflag = models.NullBooleanField()
    firm8aflag = models.NullBooleanField()
    hubzoneflag = models.NullBooleanField()
    phoneno = models.CharField(max_length=20, blank=True)
    faxno = models.CharField(max_length=20, blank=True)
    contractingofficerbusinesssizedetermination = models.CharField(max_length=1, blank=True)
    otherstatutoryauthority = models.TextField(blank=True)
    eeparentduns = models.CharField(max_length=13, blank=True)
    fiscal_year = models.IntegerField(null=True)
    mod_parent = models.CharField(max_length=100, blank=True)
    maj_agency_cat = models.CharField(max_length=2, blank=True)
    psc_cat = models.CharField(max_length=2, blank=True)
    vendor_cd = models.CharField(max_length=4, blank=True)
    pop_cd = models.CharField(max_length=4, blank=True)
    progsourceagency = models.CharField(max_length=2, blank=True)
    progsourceaccount = models.CharField(max_length=4, blank=True)
    progsourcesubacct = models.CharField(max_length=3, blank=True)
    rec_flag = models.NullBooleanField()
    type_of_contract = models.CharField(max_length=1, blank=True)    
    agency_name = models.CharField(max_length=255, blank=True)
    contracting_agency_name = models.CharField(max_length=255, blank=True)
    requesting_agency_name = models.CharField(max_length=255, blank=True)

    
