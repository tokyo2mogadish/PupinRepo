import sys
#sys.path.append(r"C:\IronPython2.7\Lib")
#import traceback
import datetime
from System import DateTime

exceptionList = []

#Provera da li Forma postoji
def getForme(Zahtev,nazivForme):
    if nazivForme in Zahtev.Forme:
        return Zahtev.Forme[nazivForme].NumerickaPoljaForme
    else:
        raise Exception('Obrazac pod nazivom: '+nazivForme+' ne postoji')


#BROJ KONVERTUJE U AOP KEY
def broj_u_aop(aop_broj, broj_kolone):
    seq = ("aop", str(aop_broj).zfill(4), str(broj_kolone))
    aop_key = "_".join(seq)
    return aop_key

#VRACA VREDNOST AOP POLJA
def aop(aop_dict, aop_broj, kolona):   
    aop_key = broj_u_aop(aop_broj, kolona)

    if aop_key in aop_dict:
        a=aop_dict[aop_key]
       
        if a is None:
            return 0
        return a

    raise Exception('Validacion skripta očekuje ' + aop_key + ' koji nije pronadjen')

    
#SUMA OD, DO ZA ZADATU KLOLONU
def suma(aop_dict, prvi_aop, poslednji_aop, kolona):
    sum = 0
    for x in range (prvi_aop, poslednji_aop+1):
        sum += aop(aop_dict, x, kolona)
    return sum

#SUMA AOPA SA LISTE
def suma_liste(aop_dict, lista, kolona):
    sum = 0
    for x in lista:
        sum += aop(aop_dict, x, kolona)
    return sum 

#LISTA NEGATIVNIH PO OBRASCU
def find_negativni(aop_dict, prvi_aop, poslednji_aop, prva_kolona, poslednja_kolona): 
    aopi = ""
    for aop_broj in range (prvi_aop,poslednji_aop+1):
        for kolona in range (prva_kolona,poslednja_kolona+1):
                aop_key = broj_u_aop(aop_broj, kolona)
                if aop_key in aop_dict:
                    a=aop_dict[aop_key]       
                    if not (a is None):
                        if a < 0 :
                            aopi += "AOP " + str(aop_broj).zfill(4) + " kol. " + str(kolona) + " = " + str(aop(aop_dict, aop_broj, kolona)) + ", "                
    if len(aopi) > 0:
         aopi = aopi.Substring(0,aopi.Length-2)
    return aopi 

#Ako forma ima bar jednu napomenu u zadatom opsegu vraca True u suprotnom False   
def proveriNapomene(aop_dict, prvi_aop, poslednji_aop, kolona):
    imaBarJednuNapomenu = False
    for aop_broj in range (prvi_aop, poslednji_aop+1):
        aop_key = broj_u_aop(aop_broj, kolona)
        if aop_dict[aop_key].strip():
            imaBarJednuNapomenu = True
            break
    return imaBarJednuNapomenu	

def Validate(Zahtev):
    try:
        doc_errors=[]
        doc_warnings=[]
        form_warnings=[]
        form_errors=[]
        ostalo_warnings = []
        ostalo_errors = []
        exceptions=[]


        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')

        #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')

        #Provera da li su prosledjeni svi ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if Zahtev.UlazniDokumenti.Count>0:
                for k in Zahtev.UlazniDokumenti.Keys:
                    if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                        doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI
        bs = getForme(Zahtev,'Bilans stanja-DUDPF')
        if len(bs)==0:
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Bilans stanja-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        bu = getForme(Zahtev,'Bilans uspeha-DUDPF')
        if len(bu)==0:
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Bilans uspeha-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        ioor = getForme(Zahtev,'Izveštaj o ostalom rezultatu-DUDPF')
        if len(ioor)==0:
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Izveštaj o ostalom rezultatu-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        iotg = getForme(Zahtev,'Izveštaj o tokovima gotovine-DUDPF')
        if len(iotg)==0:
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Izveštaj o tokovima gotovine-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        iopk = getForme(Zahtev,'Izveštaj o promenama na kapitalu-DUDPF')
        if len(iopk)==0:
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Izveštaj o promenama na kapitalu-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        si = getForme(Zahtev,'Statistički izveštaj-DUDPF')
        if len(si)==0:
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Statistički izveštaj-DUDPF nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fia = getForme(Zahtev,'Finansijski izveštaj DPF 1')
        if len(fia)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ='Finansijski izveštaj DPF 1 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fib = getForme(Zahtev,'Finansijski izveštaj DPF 2')
        if len(fib)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ='Finansijski izveštaj DPF 2 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fic = getForme(Zahtev,'Finansijski izveštaj DPF 3')
        if len(fic)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ='Finansijski izveštaj DPF 3 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fid = getForme(Zahtev,'Finansijski izveštaj DPF 4')
        if len(fid)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 4'
            poruka  ='Finansijski izveštaj DPF 4 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        fie = getForme(Zahtev,'Finansijski izveštaj DPF 5')
        if len(fie)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 5'
            poruka  ='Finansijski izveštaj DPF 5 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        hasError = False
        hasWarning = False

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################
        
        #00000-1
        if not( suma(bs,1,13,5)+suma(bs,1,13,6)+suma(bs,1,13,7)+suma(bs,401,417,5)+suma(bs,401,417,6)+suma(bs,401,417,7)+suma(bu,1001,1040,5)+suma(bu,1001,1040,6)+suma(ioor,2001,2020,5)+suma(ioor,2001,2020,6)+suma(iotg,3001,3050,3)+suma(iotg,3001,3050,4)+suma(iopk,4001,4226,1)+suma(si,9001,9028,4)+suma(si,9001,9028,5)+suma(si,9029,9036,3)+suma(si,9029,9036,4) +aop(si,9037,2) +aop(si,9039,4) +aop(si,9038,2) +aop(si,9040,4) +aop(si,9041,6) +aop(si,9042,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 + (0001 do 0013) kol. 6 + (0001 do 0013) kol. 7 bilansa stanja + (0401 do 0417) kol. 5 + (0401 do 0417) kol. 6 + (0401 do 0417) kol. 7 bilansa stanja + (1001 do 1040) kol. 5 + (1001 do 1040) kol. 6 bilansa uspeha + (2001 do 2020) kol. 5 + (2001 do 2020) kol. 6 izveštaja o ostalom rezultatu + (3001 do 3050) kol. 3 + (3001 do 3050) kol. 4 izveštaja o tokovima gotovine + (4001 do 4226) izveštaja o promenama neto imovine + (9001 do 9028) kol. 4 + (9001 do 9028) kol. 5 + (9029 do 9036) kol. 3 + (9029 do 9036) kol. 4 + (9037 do 9042) statističkog izveštaja> 0 Finansijski izveštaj ne sme biti bez podataka; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja-DUDPF'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha-DUDPF'].TekstualnaPoljaForme;
        ioorNapomene = Zahtev.Forme['Izveštaj o ostalom rezultatu-DUDPF'].TekstualnaPoljaForme;

        if not(proveriNapomene(bsNapomene, 1, 13, 4) or proveriNapomene(bsNapomene, 401, 417, 4) or proveriNapomene(buNapomene, 1001, 1040, 4) or proveriNapomene(ioorNapomene, 2001, 2020, 4)):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0013) bilansa stanja + (0401 do 0417) bilansa stanja + (1001 do 1040) bilansa uspeha + (2001 do 2020) izveštaja o ostalom rezultatu u koloni 4 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0013) bilansa stanja + (0401 do 0417) bilansa stanja + (1001 do 1040) bilansa uspeha + (2001 do 2020) izveštaja o ostalom rezultatu u koloni 4 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Na AOP-u (0001 do 0013) bilansa stanja + (0401 do 0417) bilansa stanja + (1001 do 1040) bilansa uspeha + (2001 do 2020) izveštaja o ostalom rezultatu u koloni 4 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        #ima negativni aop (408) koji je dozvoljen u obrascu bs dupf otud do 407 
        lista_bs = find_negativni(bs, 1, 407, 5, 7)
        #pa od 409 do 416 obzirom da je aopsum na 417 i tu mora da bude dozvoljena negativna vrednost
        lista_bs_2 = find_negativni(bs, 409, 416, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1040, 5, 6)
        lista_ioor = find_negativni(ioor, 2001, 2020, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3050, 3, 4)
        lista_iopk = find_negativni(iopk, 4001, 4226, 1, 1)
        lista_fia = find_negativni(fia, 1, 9042, 2, 6)
        lista_fib = find_negativni(fib, 1, 9042, 2, 6)
        lista_fic = find_negativni(fic, 1, 9042, 2, 6)
        lista_fid = find_negativni(fid, 1, 9042, 2, 6)
        lista_fie = find_negativni(fie, 1, 9042, 2, 6)
        lista_si = find_negativni(si, 9001, 9042, 2, 6)

        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bs_2) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bs_2
            else:
                lista = lista_bs_2
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista_ioor) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_ioor
            else:
                lista = lista_ioor
        if len(lista_iotg) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iotg
            else:
                lista = lista_iotg
        if len(lista_iopk) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iopk
            else:
                lista = lista_iopk
        if len(lista_fia) > 0:
           if len(lista) > 0:
               lista = lista + ", " + lista_fia
           else:
               lista = lista_fia
        if len(lista_fib) > 0:
           if len(lista) > 0:
               lista = lista + ", " + lista_fib
           else:
               lista = lista_fib
        if len(lista_fic) > 0:
           if len(lista) > 0:
               lista = lista + ", " + lista_fic
           else:
               lista = lista_fic
        if len(lista_fid) > 0:
           if len(lista) > 0:
               lista = lista + ", " + lista_fid
           else:
               lista = lista_fid
        if len(lista_fie) > 0:
           if len(lista) > 0:
               lista = lista + ", " + lista_fie
           else:
               lista = lista_fie
        if len(lista_si) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_si
            else:
                lista = lista_si
        if len(lista) > 0:                                           
            
            naziv_obrasca='Bilans stanja'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS STANJA - POTREBNO JE OBEZBEDITI UNOS IZNOSA SA PREDZNAKOM - (MINUS) NA AOP POZICIJI 0408 KOL. 5,6 I 7
        
        #00001
        if not( suma(bs,1,13,5)+suma(bs,401,417,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 5 +  (0401 do 0417) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,13,6)+suma(bs,401,417,6) == 0 ):
                lzbir =  suma(bs,1,13,6)+suma(bs,401,417,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 6 +  (0401 do 0417) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,13,7)+suma(bs,401,417,7) == 0 ):
                lzbir =  suma(bs,1,13,7)+suma(bs,401,417,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 7 +  (0401 do 0417) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,13,6)+suma(bs,401,417,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 6 +  (0401 do 0417) kol. 6 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za prethodni izveštajni period; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,13,7)+suma(bs,401,417,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0013) kol. 7 +  (0401 do 0417) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,13,5) == suma(bs,1,12,5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  suma(bs,1,12,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,13,6) == suma(bs,1,12,6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  suma(bs,1,12,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,13,7) == suma(bs,1,12,7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  suma(bs,1,12,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011 + 0012) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,408,5) == suma_liste(bs,[401,402,403,405],5)-suma_liste(bs,[404,406,407],5) ):
            lzbir =  aop(bs,408,5) 
            dzbir =  suma_liste(bs,[401,402,403,405],5)-suma_liste(bs,[404,406,407],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 5 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,408,6) == suma_liste(bs,[401,402,403,405],6)-suma_liste(bs,[404,406,407],6) ):
            lzbir =  aop(bs,408,6) 
            dzbir =  suma_liste(bs,[401,402,403,405],6)-suma_liste(bs,[404,406,407],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 6 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,408,7) == suma_liste(bs,[401,402,403,405],7)-suma_liste(bs,[404,406,407],7) ):
            lzbir =  aop(bs,408,7) 
            dzbir =  suma_liste(bs,[401,402,403,405],7)-suma_liste(bs,[404,406,407],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0408 kol. 7 = AOP-u (0401 + 0402 + 0403 - 0404 + 0405 - 0406 - 0407) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,416,5) == suma(bs,409,415,5) ):
            lzbir =  aop(bs,416,5) 
            dzbir =  suma(bs,409,415,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 5 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,416,6) == suma(bs,409,415,6) ):
            lzbir =  aop(bs,416,6) 
            dzbir =  suma(bs,409,415,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 6 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,416,7) == suma(bs,409,415,7) ):
            lzbir =  aop(bs,416,7) 
            dzbir =  suma(bs,409,415,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 7 = AOP-u (0409 + 0410 + 0411 + 0412 + 0413 + 0414 + 0415) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,417,5) == suma_liste(bs,[408,416],5) ):
            lzbir =  aop(bs,417,5) 
            dzbir =  suma_liste(bs,[408,416],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 5 = AOP-u (0408 + 0416) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,417,6) == suma_liste(bs,[408,416],6) ):
            lzbir =  aop(bs,417,6) 
            dzbir =  suma_liste(bs,[408,416],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 6 = AOP-u (0408 + 0416) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,417,7) == suma_liste(bs,[408,416],7) ):
            lzbir =  aop(bs,417,7) 
            dzbir =  suma_liste(bs,[408,416],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0417 kol. 7 = AOP-u (0408 + 0416) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,13,5) == aop(bs,417,5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  aop(bs,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u 0417 kol. 5 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,13,6) == aop(bs,417,6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  aop(bs,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u 0417 kol. 6 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,13,7) == aop(bs,417,7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  aop(bs,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u 0417 kol. 7 Kontrolno pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        #10001
        if not( suma(bu,1001,1040,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1040,6) == 0 ):
                lzbir =  suma(bu,1001,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1040,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1040) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if( aop(bu,1009,5) == suma(bu,1001,1003,5)-suma(bu,1004,1008,5) ):
            if not( suma(bu,1001,1003,5) > suma(bu,1004,1008,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1009 kol. 5 = AOP-u (1001 + 1002 + 1003 - 1004 - 1005 - 1006 - 1007 - 1008) kol. 5, ako je AOP (1001 + 1002 + 1003) kol. 5 > AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10005
        if( aop(bu,1009,6) == suma(bu,1001,1003,6)-suma(bu,1004,1008,6) ):
            if not( suma(bu,1001,1003,6) > suma(bu,1004,1008,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1009 kol. 6 = AOP-u (1001 + 1002 + 1003 - 1004 - 1005 - 1006 - 1007 - 1008) kol. 6, ako je AOP (1001 + 1002 + 1003) kol. 6 > AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10006
        if( aop(bu,1010,5) == suma(bu,1004,1008,5)-suma(bu,1001,1003,5) ):
            if not( suma(bu,1001,1003,5) < suma(bu,1004,1008,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 5 = AOP-u (1004 - 1001 - 1002 - 1003 + 1005 + 1006 + 1007 + 1008) kol. 5,  ako je AOP (1001 + 1002 + 1003) kol. 5 < AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10007
        if( aop(bu,1010,6) == suma(bu,1004,1008,6)-suma(bu,1001,1003,6) ):
            if not( suma(bu,1001,1003,6) < suma(bu,1004,1008,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 6 = AOP-u (1004 - 1001 - 1002 - 1003 + 1005 + 1006 + 1007 + 1008) kol. 6,  ako je AOP (1001 + 1002 + 1003) kol. 6 < AOP-a (1004 + 1005 + 1006 + 1007 + 1008) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10008
        if( suma(bu,1009,1010,5) == 0 ):
            if not( suma(bu,1001,1003,5) == suma(bu,1004,1008,5) ):
                lzbir =  suma(bu,1001,1003,5) 
                dzbir =  suma(bu,1004,1008,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1009 + 1010) kol. 5 = 0,  ako je AOP (1001 + 1002 + 1003) kol. 5 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( suma(bu,1009,1010,6) == 0 ):
            if not( suma(bu,1001,1003,6) == suma(bu,1004,1008,6) ):
                lzbir =  suma(bu,1001,1003,6) 
                dzbir =  suma(bu,1004,1008,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1009 + 1010) kol. 6 = 0,  ako je AOP (1001 + 1002 + 1003) kol. 6 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1009,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1009 kol. 5 > 0, onda je AOP 1010 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1009,5) == 0 ):
                lzbir =  aop(bu,1009,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 5 > 0, onda je AOP 1009 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1009,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1009 kol. 6 > 0, onda je AOP 1010 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1009,6) == 0 ):
                lzbir =  aop(bu,1009,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 6 > 0, onda je AOP 1009 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if not( suma_liste(bu,[1001,1002,1003,1010],5) == suma(bu,1004,1009,5) ):
            lzbir =  suma_liste(bu,[1001,1002,1003,1010],5) 
            dzbir =  suma(bu,1004,1009,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1002 + 1003 + 1010) kol. 5 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008 + 1009) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10015
        if not( suma_liste(bu,[1001,1002,1003,1010],6) == suma(bu,1004,1009,6) ):
            lzbir =  suma_liste(bu,[1001,1002,1003,1010],6) 
            dzbir =  suma(bu,1004,1009,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1002 + 1003 + 1010) kol. 6 = AOP-u (1004 + 1005 + 1006 + 1007 + 1008 + 1009) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10016
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1012,5) == 0 ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 5 > 0, onda je AOP 1012 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( aop(bu,1012,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 5 > 0, onda je AOP 1011 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1012,6) == 0 ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 6 > 0, onda je AOP 1012 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1012,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 6 > 0, onda je AOP 1011 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1013,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1013 kol. 5 > 0, onda je AOP 1014 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1013,5) == 0 ):
                lzbir =  aop(bu,1013,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 5 > 0, onda je AOP 1013 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1013,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1013 kol. 6 > 0, onda je AOP 1014 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1013,6) == 0 ):
                lzbir =  aop(bu,1013,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 6 > 0, onda je AOP 1013 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1016,5) == 0 ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 5 > 0, onda je AOP 1016 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1016,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 5 > 0, onda je AOP 1015 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1016,6) == 0 ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 6 > 0, onda je AOP 1016 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1016,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 6 > 0, onda je AOP 1015 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1017,5) > 0 ):
            if not( aop(bu,1018,5) == 0 ):
                lzbir =  aop(bu,1018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 5 > 0, onda je AOP 1018 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1018,5) > 0 ):
            if not( aop(bu,1017,5) == 0 ):
                lzbir =  aop(bu,1017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 5 > 0, onda je AOP 1017 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1017,6) > 0 ):
            if not( aop(bu,1018,6) == 0 ):
                lzbir =  aop(bu,1018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 6 > 0, onda je AOP 1018 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1018,6) > 0 ):
            if not( aop(bu,1017,6) == 0 ):
                lzbir =  aop(bu,1017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 6 > 0, onda je AOP 1017 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1019,5) > 0 ):
            if not( aop(bu,1020,5) == 0 ):
                lzbir =  aop(bu,1020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 5 > 0, onda je AOP 1020 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1020,5) > 0 ):
            if not( aop(bu,1019,5) == 0 ):
                lzbir =  aop(bu,1019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 5 > 0, onda je AOP 1019 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1019,6) > 0 ):
            if not( aop(bu,1020,6) == 0 ):
                lzbir =  aop(bu,1020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1019 kol. 6 > 0, onda je AOP 1020 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1020,6) > 0 ):
            if not( aop(bu,1019,6) == 0 ):
                lzbir =  aop(bu,1019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1020 kol. 6 > 0, onda je AOP 1019 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i neto gubici '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1021,5) > 0 ):
            if not( aop(bu,1022,5) == 0 ):
                lzbir =  aop(bu,1022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 5 > 0, onda je AOP 1022 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1022,5) > 0 ):
            if not( aop(bu,1021,5) == 0 ):
                lzbir =  aop(bu,1021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 5 > 0, onda je AOP 1021 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1021,6) > 0 ):
            if not( aop(bu,1022,6) == 0 ):
                lzbir =  aop(bu,1022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 6 > 0, onda je AOP 1022 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1022,6) > 0 ):
            if not( aop(bu,1021,6) == 0 ):
                lzbir =  aop(bu,1021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 6 > 0, onda je AOP 1021 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani neto prihodi i neto rashodi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if( aop(bu,1032,5) == suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) > suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025 - 1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 5, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 > AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( aop(bu,1032,6) == suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6)-suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) > suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1009 - 1010 + 1011 - 1012 + 1013 - 1014 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022 + 1023 - 1024 + 1025 - 1026 - 1027 - 1028 - 1029 + 1030 - 1031) kol. 6, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 > AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( aop(bu,1033,5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) < suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 5 = AOP-u (1010 - 1009 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025 + 1026 + 1027 + 1028 + 1029 - 1030 + 1031) kol. 5,  ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 < AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( aop(bu,1033,6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6)-suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) < suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1033 kol. 6 = AOP-u (1010 - 1009 - 1011 + 1012 - 1013 + 1014 - 1015 + 1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025 + 1026 + 1027 + 1028 + 1029 - 1030 + 1031) kol. 6,  ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 < AOP-a (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( suma(bu,1032,1033,5) == 0 ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) ):
                lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],5) 
                dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 5 =  0, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 5 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( suma(bu,1032,1033,6) == 0 ):
            if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) ):
                lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030],6) 
                dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1032 + 1033) kol. 6 =  0, ako je AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030) kol. 6 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1033,5) == 0 ):
                lzbir =  aop(bu,1033,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0, onda je AOP 1033 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( aop(bu,1033,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 5 > 0, onda je AOP 1032 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1033,6) == 0 ):
                lzbir =  aop(bu,1033,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0, onda je AOP 1033 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1033,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1033 kol. 6 > 0, onda je AOP 1032 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],5) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],5) ):
            lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],5) 
            dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030 + 1033) kol. 5 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031 + 1032) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10051
        if not( suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],6) == suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],6) ):
            lzbir =  suma_liste(bu,[1009,1011,1013,1015,1017,1019,1021,1023,1025,1030,1033],6) 
            dzbir =  suma_liste(bu,[1010,1012,1014,1016,1018,1020,1022,1024,1026,1027,1028,1029,1031,1032],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1009 + 1011 + 1013 + 1015 + 1017 + 1019 + 1021 + 1023 + 1025 + 1030 + 1033) kol. 6 = AOP-u (1010 + 1012 + 1014  + 1016 + 1018 + 1020 + 1022 + 1024 + 1026 + 1027 + 1028 + 1029 + 1031 + 1032) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1039,5) == suma_liste(bu,[1032,1034,1036],5)-suma_liste(bu,[1033,1035,1037,1038],5) ):
            if not( suma_liste(bu,[1032,1034,1036],5) > suma_liste(bu,[1033,1035,1037,1038],5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 5 = AOP-u (1032 - 1033 + 1034 - 1035 + 1036 - 1037 - 1038) kol. 5 , ako je AOP (1032 + 1034 + 1036) kol. 5 > AOP-a (1033 + 1035 + 1037 + 1038) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1039,6) == suma_liste(bu,[1032,1034,1036],6)-suma_liste(bu,[1033,1035,1037,1038],6) ):
            if not( suma_liste(bu,[1032,1034,1036],6) > suma_liste(bu,[1033,1035,1037,1038],6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 6 = AOP-u (1032 - 1033 + 1034 - 1035 + 1036 - 1037 - 1038) kol. 6 , ako je AOP (1032 + 1034 + 1036) kol. 6 > AOP-a (1033 + 1035 + 1037 + 1038) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1040,5) == suma_liste(bu,[1033,1035,1037,1038],5)-suma_liste(bu,[1032,1034,1036],5) ):
            if not( suma_liste(bu,[1032,1034,1036],5) < suma_liste(bu,[1033,1035,1037,1038],5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 5 = AOP-u (1033 - 1032 - 1034 + 1035 - 1036 + 1037 + 1038) kol. 5, ako je AOP (1032 + 1034 + 1036) kol. 5 < AOP-a (1033 + 1035 + 1037 + 1038) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1040,6) == suma_liste(bu,[1033,1035,1037,1038],6)-suma_liste(bu,[1032,1034,1036],6) ):
            if not( suma_liste(bu,[1032,1034,1036],6) < suma_liste(bu,[1033,1035,1037,1038],6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1040 kol. 6 = AOP-u (1033 - 1032 - 1034 + 1035 - 1036 + 1037 + 1038) kol. 6, ako je AOP (1032 + 1034 + 1036) kol. 6 < AOP-a (1033 + 1035 + 1037 + 1038) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( suma(bu,1039,1040,5) == 0 ):
            if not( suma_liste(bu,[1032,1034,1036],5) == suma_liste(bu,[1033,1035,1037,1038],5) ):
                lzbir =  suma_liste(bu,[1032,1034,1036],5) 
                dzbir =  suma_liste(bu,[1033,1035,1037,1038],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1039 + 1040) kol. 5 = 0, ako je AOP (1032 + 1034 + 1036) kol. 5 = AOP-u (1033 + 1035 + 1037 + 1038) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( suma(bu,1039,1040,6) == 0 ):
            if not( suma_liste(bu,[1032,1034,1036],6) == suma_liste(bu,[1033,1035,1037,1038],6) ):
                lzbir =  suma_liste(bu,[1032,1034,1036],6) 
                dzbir =  suma_liste(bu,[1033,1035,1037,1038],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1039 + 1040) kol. 6 = 0, ako je AOP (1032 + 1034 + 1036) kol. 6 = AOP-u (1033 + 1035 + 1037 + 1038) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1040,5) == 0 ):
                lzbir =  aop(bu,1040,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP 1040 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10059
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 1039 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10060
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1040,6) == 0 ):
                lzbir =  aop(bu,1040,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP 1040 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10061
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 1039 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if not( suma_liste(bu,[1032,1034,1036,1040],5) == suma_liste(bu,[1033,1035,1037,1038,1039],5) ):
            lzbir =  suma_liste(bu,[1032,1034,1036,1040],5) 
            dzbir =  suma_liste(bu,[1033,1035,1037,1038,1039],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1034 + 1036 + 1040) kol. 5 = AOP-u (1033 + 1035 + 1037 + 1038 + 1039) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10063
        if not( suma_liste(bu,[1032,1034,1036,1040],6) == suma_liste(bu,[1033,1035,1037,1038,1039],6) ):
            lzbir =  suma_liste(bu,[1032,1034,1036,1040],6) 
            dzbir =  suma_liste(bu,[1033,1035,1037,1038,1039],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1032 + 1034 + 1036 + 1040) kol. 6 = AOP-u (1033 + 1035 + 1037 + 1038 + 1039) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10064
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bs,405,5) >= aop(bu,1039,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP  0405 kol. 5 bilansa stanja ≥ AOP-a 1039 kol. 5  Dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP  0405 kol. 5 bilansa stanja ≥ AOP-a 1039 kol. 5  Dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni tekuća godina u obrascu Bilans stanja; Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bs,405,6) >= aop(bu,1039,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP  0405 kol. 6 bilansa stanja ≥ AOP-a 1039 kol. 6 Dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP  0405 kol. 6 bilansa stanja ≥ AOP-a 1039 kol. 6 Dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu neraspoređenog dobitka u koloni prethodna godina u obrascu Bilans stanja.  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10066
        if( aop(bu,1040,5) > 0 ):
            if not( aop(bs,406,5) >= aop(bu,1040,5) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 0406 kol. 5 bilansa stanja ≥ AOP-a 1040 kol. 5  Gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1040 kol. 5 > 0, onda je AOP 0406 kol. 5 bilansa stanja ≥ AOP-a 1040 kol. 5  Gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni tekuća godina u obrascu Bilans stanja;  Ukoliko ti podaci nisu usaglašeni, zakonski zastupnik potpisivanjem izveštaja potvrđuje da je tako iskazan rezultat u Bilansu stanja ispravan i tačan, odnosno da je iskazan u skladu sa propisima. '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10067
        if( aop(bu,1040,6) > 0 ):
            if not( aop(bs,406,6) >= aop(bu,1040,6) ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 0406 kol. 6 bilansa stanja ≥ AOP-a 1040 kol. 6 Gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1040 kol. 6 > 0, onda je AOP 0406 kol. 6 bilansa stanja ≥ AOP-a 1040 kol. 6 Gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti manji ili jednak iznosu gubitka u koloni prethodna godina u obrascu Bilans stanja.   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O OSTALOM REZULTATU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #20001
        if not( suma(ioor,2001,2020,5) > 0 ):
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='Zbir podataka na oznakama za AOP (2001 do 2020) kol. 5 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #20002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(ioor,2001,2020,6) == 0 ):
                lzbir =  suma(ioor,2001,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2020) kol. 6 = 0 Izveštaj o ostalom rezultatu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(ioor,2001,2020,6) > 0 ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Zbir podataka na oznakama za AOP (2001 do 2020) kol. 6 > 0 Izveštaj o ostalom rezultatu, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #20004
        if not( aop(ioor,2001,5) == aop(bu,1039,5) ):
            lzbir =  aop(ioor,2001,5) 
            dzbir =  aop(bu,1039,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1039 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 5 = AOP-u 1039 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20005
        if not( aop(ioor,2001,6) == aop(bu,1039,6) ):
            lzbir =  aop(ioor,2001,6) 
            dzbir =  aop(bu,1039,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1039 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2001 kol. 6 = AOP-u 1039 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20006
        if not( aop(ioor,2002,5) == aop(bu,1040,5) ):
            lzbir =  aop(ioor,2002,5) 
            dzbir =  aop(bu,1040,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1040 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 5 = AOP-u 1040 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20007
        if not( aop(ioor,2002,6) == aop(bu,1040,6) ):
            lzbir =  aop(ioor,2002,6) 
            dzbir =  aop(bu,1040,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1040 kol.6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP 2002 kol. 6 = AOP-u 1040 kol.6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20008
        if( aop(ioor,2017,5) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5) ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2017 kol. 5 = AOP (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 5 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 +2016) kol. 5   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20009
        if( aop(ioor,2017,6) == suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6)-suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6) ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6) > suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2017 kol. 6 = AOP (2003 - 2004 + 2005 - 2006 + 2007 - 2008 + 2009 - 2010 + 2011 - 2012 + 2013 - 2014 + 2015 - 2016) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 6 > AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 +2016) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20010
        if( aop(ioor,2018,5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5) ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2018 kol. 5 = AOP-u (2004 - 2003 - 2005 + 2006 - 2007 + 2008 - 2009 + 2010 - 2011 + 2012 - 2013 + 2014 - 2015 + 2016) kol. 5, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 5 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016) kol. 5   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20011
        if( aop(ioor,2018,6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6)-suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6) ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6) < suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2018 kol. 6 = AOP-u (2004 - 2003 - 2005 + 2006 - 2007 + 2008 - 2009 + 2010 - 2011 + 2012 - 2013 + 2014 - 2015 + 2016) kol. 6, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 6 < AOP-a (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016) kol. 6   '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20012
        if( suma(ioor,2017,2018,5) == 0 ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5) ):
                lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],5) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2017 + 2018) kol. 5 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016) kol. 5  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20013
        if( suma(ioor,2017,2018,6) == 0 ):
            if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6) ):
                lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015],6) 
                dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2017 + 2018) kol. 6 = 0, ako je AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016) kol. 6  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20014
        if( aop(ioor,2017,5) > 0 ):
            if not( aop(ioor,2018,5) == 0 ):
                lzbir =  aop(ioor,2018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2017 kol. 5 > 0, onda je AOP 2018 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ostali ukupan dobitak i ostali ukupan gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20015
        if( aop(ioor,2018,5) > 0 ):
            if not( aop(ioor,2017,5) == 0 ):
                lzbir =  aop(ioor,2017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2018 kol. 5 > 0, onda je AOP 2017 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ostali ukupan dobitak i ostali ukupan gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20016
        if( aop(ioor,2017,6) > 0 ):
            if not( aop(ioor,2018,6) == 0 ):
                lzbir =  aop(ioor,2018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2017 kol. 6 > 0, onda je AOP 2018 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ostali ukupan dobitak i ostali ukupan gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20017
        if( aop(ioor,2018,6) > 0 ):
            if not( aop(ioor,2017,6) == 0 ):
                lzbir =  aop(ioor,2017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2018 kol. 6 > 0, onda je AOP 2017 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ostali ukupan dobitak i ostali ukupan gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20018
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2018],5) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2017],5) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2018],5) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2017],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2018) kol. 5 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2017) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20019
        if not( suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2018],6) == suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2017],6) ):
            lzbir =  suma_liste(ioor,[2003,2005,2007,2009,2011,2013,2015,2018],6) 
            dzbir =  suma_liste(ioor,[2004,2006,2008,2010,2012,2014,2016,2017],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2003 + 2005 + 2007 + 2009 + 2011 + 2013 + 2015 + 2018) kol. 6 = AOP-u (2004 + 2006 + 2008 + 2010 + 2012 + 2014 + 2016 + 2017) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20020
        if( aop(ioor,2019,5) == suma_liste(ioor,[2001,2017],5)-suma_liste(ioor,[2002,2018],5) ):
            if not( suma_liste(ioor,[2001,2017],5) > suma_liste(ioor,[2002,2018],5) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2019 kol. 5 = AOP-u (2001 - 2002 + 2017 - 2018) kol. 5, ako je AOP (2001 + 2017) kol. 5 > AOP-a (2002 + 2018) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20021
        if( aop(ioor,2019,6) == suma_liste(ioor,[2001,2017],6)-suma_liste(ioor,[2002,2018],6) ):
            if not( suma_liste(ioor,[2001,2017],6) > suma_liste(ioor,[2002,2018],6) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2019 kol. 6 = AOP-u (2001 - 2002 + 2017 - 2018) kol. 6, ako je AOP (2001 + 2017) kol. 6 > AOP-a (2002 + 2018) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20022
        if( aop(ioor,2020,5) == suma_liste(ioor,[2002,2018],5)-suma_liste(ioor,[2001,2017],5) ):
            if not( suma_liste(ioor,[2001,2017],5) < suma_liste(ioor,[2002,2018],5) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2020 kol. 5 = AOP-u (2002 - 2001 - 2017 + 2018) kol. 5, ako je AOP (2001 + 2017) kol. 5 < AOP-a (2002 + 2018) kol. 5  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20023
        if( aop(ioor,2020,6) == suma_liste(ioor,[2002,2018],6)-suma_liste(ioor,[2001,2017],6) ):
            if not( suma_liste(ioor,[2001,2017],6) < suma_liste(ioor,[2002,2018],6) ):
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP 2020 kol. 6 = AOP-u (2002 - 2001 - 2017 + 2018) kol. 6, ako je AOP (2001 + 2017) kol. 6 < AOP-a (2002 + 2018) kol. 6  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20024
        if( suma(ioor,2019,2020,5) == 0 ):
            if not( suma_liste(ioor,[2001,2017],5) == suma_liste(ioor,[2002,2018],5) ):
                lzbir =  suma_liste(ioor,[2001,2017],5) 
                dzbir =  suma_liste(ioor,[2002,2018],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2019 + 2020) kol. 5 = 0, ako je AOP (2001 + 2017) kol. 5 = AOP-u (2002 + 2018) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20025
        if( suma(ioor,2019,2020,6) == 0 ):
            if not( suma_liste(ioor,[2001,2017],6) == suma_liste(ioor,[2002,2018],6) ):
                lzbir =  suma_liste(ioor,[2001,2017],6) 
                dzbir =  suma_liste(ioor,[2002,2018],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='AOP (2019 + 2020) kol. 6 = 0, ako je AOP (2001 + 2017) kol. 6 = AOP-u (2002 + 2018) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20026
        if( aop(ioor,2019,5) > 0 ):
            if not( aop(ioor,2020,5) == 0 ):
                lzbir =  aop(ioor,2020,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2019 kol. 5 > 0, onda je AOP 2020 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto dobitak i ukupan neto gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20027
        if( aop(ioor,2020,5) > 0 ):
            if not( aop(ioor,2019,5) == 0 ):
                lzbir =  aop(ioor,2019,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2020 kol. 5 > 0, onda je AOP 2019 kol. 5 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto dobitak i ukupan neto gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20028
        if( aop(ioor,2019,6) > 0 ):
            if not( aop(ioor,2020,6) == 0 ):
                lzbir =  aop(ioor,2020,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2019 kol. 6 > 0, onda je AOP 2020 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto dobitak i ukupan neto gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20029
        if( aop(ioor,2020,6) > 0 ):
            if not( aop(ioor,2019,6) == 0 ):
                lzbir =  aop(ioor,2019,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o ostalom rezultatu'
                poruka  ='Ako je AOP 2020 kol. 6 > 0, onda je AOP 2019 kol. 6 = 0 U Izveštaju o ostalom rezultatu ne mogu biti istovremeno prikazani ukupan neto dobitak i ukupan neto gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #20030
        if not( suma_liste(ioor,[2001,2017,2020],5) == suma_liste(ioor,[2002,2018,2019],5) ):
            lzbir =  suma_liste(ioor,[2001,2017,2020],5) 
            dzbir =  suma_liste(ioor,[2002,2018,2019],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2017 + 2020) kol. 5 = AOP-u (2002 + 2018 + 2019) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #20031
        if not( suma_liste(ioor,[2001,2017,2020],6) == suma_liste(ioor,[2002,2018,2019],6) ):
            lzbir =  suma_liste(ioor,[2001,2017,2020],6) 
            dzbir =  suma_liste(ioor,[2002,2018,2019],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o ostalom rezultatu'
            poruka  ='AOP (2001 + 2017 + 2020) kol. 6 = AOP-u (2002 + 2018 + 2019) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3050,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3050) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3050,4) == 0 ):
                lzbir =  suma(iotg,3001,3050,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3050) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3050,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3050) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #30004
        if not( aop(iotg,3001,3) == suma(iotg,3002,3005,3) ):
            lzbir =  aop(iotg,3001,3) 
            dzbir =  suma(iotg,3002,3005,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30005
        if not( aop(iotg,3001,4) == suma(iotg,3002,3005,4) ):
            lzbir =  aop(iotg,3001,4) 
            dzbir =  suma(iotg,3002,3005,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30006
        if not( aop(iotg,3006,3) == suma(iotg,3007,3012,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3012,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3006,4) == suma(iotg,3007,3012,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3012,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3013,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
            if not( aop(iotg,3001,3) > aop(iotg,3006,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3013 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3013,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
            if not( aop(iotg,3001,4) > aop(iotg,3006,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3013 kol. 4 = AOP-u (3001 - 3006) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3014,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
            if not( aop(iotg,3001,3) < aop(iotg,3006,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 3 = AOP-u (3006 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3014,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
            if not( aop(iotg,3001,4) < aop(iotg,3006,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 4 = AOP-u (3006 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( suma(iotg,3013,3014,3) == 0 ):
            if not( aop(iotg,3001,3) == aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3001,3) 
                dzbir =  aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3013 + 3014) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( suma(iotg,3013,3014,4) == 0 ):
            if not( aop(iotg,3001,4) == aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3001,4) 
                dzbir =  aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3013 + 3014) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3013,3) > 0 ):
            if not( aop(iotg,3014,3) == 0 ):
                lzbir =  aop(iotg,3014,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3013 kol. 3 > 0, onda je AOP 3014 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3014,3) > 0 ):
            if not( aop(iotg,3013,3) == 0 ):
                lzbir =  aop(iotg,3013,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 3 > 0, onda je AOP 3013 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3013,4) > 0 ):
            if not( aop(iotg,3014,4) == 0 ):
                lzbir =  aop(iotg,3014,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3013 kol. 4 > 0, onda je AOP 3014 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3014,4) > 0 ):
            if not( aop(iotg,3013,4) == 0 ):
                lzbir =  aop(iotg,3013,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 4 > 0, onda je AOP 3013 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3014],3) == suma_liste(iotg,[3006,3013],3) ):
            lzbir =  suma_liste(iotg,[3001,3014],3) 
            dzbir =  suma_liste(iotg,[3006,3013],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3014) kol. 3 = AOP-u (3006 + 3013) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3014],4) == suma_liste(iotg,[3006,3013],4) ):
            lzbir =  suma_liste(iotg,[3001,3014],4) 
            dzbir =  suma_liste(iotg,[3006,3013],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3014) kol. 4 = AOP-u (3006 + 3013) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3015,3) == suma(iotg,3016,3020,3) ):
            lzbir =  aop(iotg,3015,3) 
            dzbir =  suma(iotg,3016,3020,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3015 kol. 3 = AOP-u (3016 + 3017 + 3018 + 3019 + 3020) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3015,4) == suma(iotg,3016,3020,4) ):
            lzbir =  aop(iotg,3015,4) 
            dzbir =  suma(iotg,3016,3020,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3015 kol. 4 = AOP-u (3016 + 3017 + 3018 + 3019 + 3020) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30022
        if not( aop(iotg,3021,3) == suma(iotg,3022,3025,3) ):
            lzbir =  aop(iotg,3021,3) 
            dzbir =  suma(iotg,3022,3025,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3021 kol. 3 = AOP-u (3022 + 3023 + 3024 + 3025) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30023
        if not( aop(iotg,3021,4) == suma(iotg,3022,3025,4) ):
            lzbir =  aop(iotg,3021,4) 
            dzbir =  suma(iotg,3022,3025,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3021 kol. 4 = AOP-u (3022 + 3023 + 3024 + 3025) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30024
        if( aop(iotg,3026,3) == aop(iotg,3015,3)-aop(iotg,3021,3) ):
            if not( aop(iotg,3015,3) > aop(iotg,3021,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 3 = AOP-u (3015 - 3021) kol. 3, ako je AOP 3015 kol. 3 > AOP-a 3021 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3026,4) == aop(iotg,3015,4)-aop(iotg,3021,4) ):
            if not( aop(iotg,3015,4) > aop(iotg,3021,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 4 = AOP-u (3015 - 3021) kol. 4, ako je AOP 3015 kol. 4 > AOP-a 3021 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3027,3) == aop(iotg,3021,3)-aop(iotg,3015,3) ):
            if not( aop(iotg,3015,3) < aop(iotg,3021,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 3 = AOP-u (3021 - 3015) kol. 3, ako je AOP 3015 kol. 3 < AOP-a 3021 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3027,4) == aop(iotg,3021,4)-aop(iotg,3015,4) ):
            if not( aop(iotg,3015,4) < aop(iotg,3021,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 4 = AOP-u (3021 - 3015) kol. 4, ako je AOP 3015 kol. 4 < AOP-a 3021 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( suma(iotg,3026,3027,3) == 0 ):
            if not( aop(iotg,3015,3) == aop(iotg,3021,3) ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  aop(iotg,3021,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3026 + 3027) kol. 3 = 0, ako je AOP 3015 kol. 3 = AOP-u 3021 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( suma(iotg,3026,3027,4) == 0 ):
            if not( aop(iotg,3015,4) == aop(iotg,3021,4) ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  aop(iotg,3021,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3026 + 3027) kol. 4 = 0, ako je AOP 3015 kol. 4 = AOP-u 3021 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30030
        if( aop(iotg,3026,3) > 0 ):
            if not( aop(iotg,3027,3) == 0 ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3026 kol. 3 > 0, onda je AOP 3027 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30031
        if( aop(iotg,3027,3) > 0 ):
            if not( aop(iotg,3026,3) == 0 ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 3 > 0, onda je AOP 3026 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30032
        if( aop(iotg,3026,4) > 0 ):
            if not( aop(iotg,3027,4) == 0 ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3026 kol. 4 > 0, onda je AOP 3027 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30033
        if( aop(iotg,3027,4) > 0 ):
            if not( aop(iotg,3026,4) == 0 ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3027 kol. 4 > 0, onda je AOP 3026 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30034
        if not( suma_liste(iotg,[3015,3027],3) == suma_liste(iotg,[3021,3026],3) ):
            lzbir =  suma_liste(iotg,[3015,3027],3) 
            dzbir =  suma_liste(iotg,[3021,3026],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3015 + 3027) kol. 3 = AOP-u (3021 + 3026) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3015,3027],4) == suma_liste(iotg,[3021,3026],4) ):
            lzbir =  suma_liste(iotg,[3015,3027],4) 
            dzbir =  suma_liste(iotg,[3021,3026],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3015 + 3027) kol. 4 = AOP-u (3021 + 3026) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if not( aop(iotg,3028,3) == suma(iotg,3029,3033,3) ):
            lzbir =  aop(iotg,3028,3) 
            dzbir =  suma(iotg,3029,3033,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3028 kol. 3 = AOP-u (3029 + 3030 + 3031 + 3032 + 3033) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30037
        if not( aop(iotg,3028,4) == suma(iotg,3029,3033,4) ):
            lzbir =  aop(iotg,3028,4) 
            dzbir =  suma(iotg,3029,3033,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3028 kol. 4 = AOP-u (3029 + 3030 + 3031 + 3032 + 3033) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30038
        if not( aop(iotg,3034,3) == suma(iotg,3035,3040,3) ):
            lzbir =  aop(iotg,3034,3) 
            dzbir =  suma(iotg,3035,3040,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3034 kol. 3 = AOP-u (3035 + 3036 + 3037 + 3038 + 3039 + 3040) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30039
        if not( aop(iotg,3034,4) == suma(iotg,3035,3040,4) ):
            lzbir =  aop(iotg,3034,4) 
            dzbir =  suma(iotg,3035,3040,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3034 kol. 4 = AOP-u (3035 + 3036 + 3037 + 3038 + 3039 + 3040) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30040
        if( aop(iotg,3041,3) == aop(iotg,3028,3)-aop(iotg,3034,3) ):
            if not( aop(iotg,3028,3) > aop(iotg,3034,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3041 kol. 3 = AOP-u (3028 - 3034) kol. 3, ako je AOP 3028 kol. 3 > AOP-a 3034 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( aop(iotg,3041,4) == aop(iotg,3028,4)-aop(iotg,3034,4) ):
            if not( aop(iotg,3028,4) > aop(iotg,3034,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3041 kol. 4 = AOP-u (3028 - 3034) kol. 4, ako je AOP 3028 kol. 4 > AOP-a 3034 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
        if( aop(iotg,3042,3) == aop(iotg,3034,3)-aop(iotg,3028,3) ):
            if not( aop(iotg,3028,3) < aop(iotg,3034,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3042 kol. 3 = AOP-u (3034 - 3028) kol. 3, ako je AOP 3028 kol. 3 < AOP-a 3034 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30043
        if( aop(iotg,3042,4) == aop(iotg,3034,4)-aop(iotg,3028,4) ):
            if not( aop(iotg,3028,4) < aop(iotg,3034,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3042 kol. 4 = AOP-u (3034 - 3028) kol. 4, ako je AOP 3028 kol. 4 < AOP-a 3034 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30044
        if( suma(iotg,3041,3042,3) == 0 ):
            if not( aop(iotg,3028,3) == aop(iotg,3034,3) ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  aop(iotg,3034,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3041 + 3042)  kol. 3 = 0, ako je AOP 3028 kol. 3 = AOP-u 3034 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30045
        if( suma(iotg,3041,3042,4) == 0 ):
            if not( aop(iotg,3028,4) == aop(iotg,3034,4) ):
                lzbir =  aop(iotg,3028,4) 
                dzbir =  aop(iotg,3034,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3041 + 3042)  kol. 4 = 0, ako je AOP 3028 kol. 4 = AOP-u 3034 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30046
        if( aop(iotg,3041,3) > 0 ):
            if not( aop(iotg,3042,3) == 0 ):
                lzbir =  aop(iotg,3042,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3041 kol. 3 > 0, onda je AOP 3042 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30047
        if( aop(iotg,3042,3) > 0 ):
            if not( aop(iotg,3041,3) == 0 ):
                lzbir =  aop(iotg,3041,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3042 kol. 3 > 0, onda je AOP 3041 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30048
        if( aop(iotg,3041,4) > 0 ):
            if not( aop(iotg,3042,4) == 0 ):
                lzbir =  aop(iotg,3042,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3041 kol. 4 > 0, onda je AOP 3042 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( aop(iotg,3042,4) > 0 ):
            if not( aop(iotg,3041,4) == 0 ):
                lzbir =  aop(iotg,3041,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3042 kol. 4 > 0, onda je AOP 3041 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if not( suma_liste(iotg,[3028,3042],3) == suma_liste(iotg,[3034,3041],3) ):
            lzbir =  suma_liste(iotg,[3028,3042],3) 
            dzbir =  suma_liste(iotg,[3034,3041],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3028 + 3042) kol. 3 = AOP-u (3034 + 3041) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30051
        if not( suma_liste(iotg,[3028,3042],4) == suma_liste(iotg,[3034,3041],4) ):
            lzbir =  suma_liste(iotg,[3028,3042],4) 
            dzbir =  suma_liste(iotg,[3034,3041],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3028 + 3042) kol. 4 = AOP-u (3034 + 3041) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30052
        if not( aop(iotg,3043,3) == suma_liste(iotg,[3013,3026,3041],3) ):
            lzbir =  aop(iotg,3043,3) 
            dzbir =  suma_liste(iotg,[3013,3026,3041],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3043 kol. 3 = AOP-u (3013 + 3026 + 3041) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30053
        if not( aop(iotg,3043,4) == suma_liste(iotg,[3013,3026,3041],4) ):
            lzbir =  aop(iotg,3043,4) 
            dzbir =  suma_liste(iotg,[3013,3026,3041],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3043 kol. 4 = AOP-u (3013 + 3026 + 3041) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30054
        if not( aop(iotg,3044,3) == suma_liste(iotg,[3014,3027,3042],3) ):
            lzbir =  aop(iotg,3044,3) 
            dzbir =  suma_liste(iotg,[3014,3027,3042],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3044 kol. 3 = AOP-u (3014 + 3027 + 3042) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30055
        if not( aop(iotg,3044,4) == suma_liste(iotg,[3014,3027,3042],4) ):
            lzbir =  aop(iotg,3044,4) 
            dzbir =  suma_liste(iotg,[3014,3027,3042],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3044 kol. 4 = AOP-u (3014 + 3027 + 3042) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30056
        if( aop(iotg,3045,3) == aop(iotg,3043,3)-aop(iotg,3044,3) ):
            if not( aop(iotg,3043,3) > aop(iotg,3044,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 3 = AOP-u (3043 - 3044) kol. 3, ako je AOP 3043 kol. 3 > AOP-a 3044 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30057
        if( aop(iotg,3045,4) == aop(iotg,3043,4)-aop(iotg,3044,4) ):
            if not( aop(iotg,3043,4) > aop(iotg,3044,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3045 kol. 4 = AOP-u (3043 - 3044) kol. 4, ako je AOP 3043 kol. 4 > AOP-a 3044 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30058
        if( aop(iotg,3046,3) == aop(iotg,3044,3)-aop(iotg,3043,3) ):
            if not( aop(iotg,3043,3) < aop(iotg,3044,3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 3 = AOP-u (3044 - 3043) kol. 3, ako je AOP 3043 kol. 3 < AOP-a 3044 kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30059
        if( aop(iotg,3046,4) == aop(iotg,3044,4)-aop(iotg,3043,4) ):
            if not( aop(iotg,3043,4) < aop(iotg,3044,4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3046 kol. 4 = AOP-u (3044 - 3043) kol. 4, ako je AOP 3043 kol. 4 < AOP-a 3044 kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30060
        if( suma(iotg,3045,3046,3) == 0 ):
            if not( aop(iotg,3043,3) == aop(iotg,3044,3) ):
                lzbir =  aop(iotg,3043,3) 
                dzbir =  aop(iotg,3044,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3045 + 3046) kol. 3 = 0, ako je AOP 3043 kol. 3 = AOP-u 3044 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30061
        if( suma(iotg,3045,3046,4) == 0 ):
            if not( aop(iotg,3043,4) == aop(iotg,3044,4) ):
                lzbir =  aop(iotg,3043,4) 
                dzbir =  aop(iotg,3044,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3045 + 3046) kol. 4 = 0, ako je AOP 3043 kol. 4 = AOP-u 3044 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30062
        if( aop(iotg,3045,3) > 0 ):
            if not( aop(iotg,3046,3) == 0 ):
                lzbir =  aop(iotg,3046,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 3 > 0, onda je AOP 3046 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30063
        if( aop(iotg,3046,3) > 0 ):
            if not( aop(iotg,3045,3) == 0 ):
                lzbir =  aop(iotg,3045,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 3 > 0, onda je AOP 3045 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30064
        if( aop(iotg,3045,4) > 0 ):
            if not( aop(iotg,3046,4) == 0 ):
                lzbir =  aop(iotg,3046,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3045 kol. 4 > 0, onda je AOP 3046 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30065
        if( aop(iotg,3046,4) > 0 ):
            if not( aop(iotg,3045,4) == 0 ):
                lzbir =  aop(iotg,3045,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3046 kol. 4 > 0, onda je AOP 3045 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja gotovine '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30066
        if not( suma_liste(iotg,[3043,3046],3) == suma(iotg,3044,3045,3) ):
            lzbir =  suma_liste(iotg,[3043,3046],3) 
            dzbir =  suma(iotg,3044,3045,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3043 + 3046) kol. 3 = AOP-u (3044 + 3045) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30067
        if not( suma_liste(iotg,[3043,3046],4) == suma(iotg,3044,3045,4) ):
            lzbir =  suma_liste(iotg,[3043,3046],4) 
            dzbir =  suma(iotg,3044,3045,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3043 + 3046) kol. 4 = AOP-u (3044 + 3045) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30068
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3047,3) == 0 ):
                lzbir =  aop(iotg,3047,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3047 kol. 3 = 0 Novoosnovana pravna lica ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30069
        if( aop(iotg,3050,3) == suma_liste(iotg,[3045,3047,3048],3)-suma_liste(iotg,[3046,3049],3) ):
            if not( suma_liste(iotg,[3045,3047,3048],3) > suma_liste(iotg,[3046,3049],3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 3 = AOP-u (3045 - 3046 + 3047 + 3048 - 3049) kol. 3, ako je AOP (3045 + 3047 + 3048) kol. 3 > AOP-a (3046 + 3049) kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30070
        if( aop(iotg,3050,4) == suma_liste(iotg,[3045,3047,3048],4)-suma_liste(iotg,[3046,3049],4) ):
            if not( suma_liste(iotg,[3045,3047,3048],4) > suma_liste(iotg,[3046,3049],4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 4 = AOP-u (3045 - 3046 + 3047 + 3048 - 3049) kol. 4, ako je AOP (3045 + 3047 + 3048) kol. 4 > AOP-a (3046 + 3049) kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30071
        if( aop(iotg,3050,3) == 0 ):
            if not( suma_liste(iotg,[3045,3047,3048],3) <= suma_liste(iotg,[3046,3049],3) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 3 = 0, ako je AOP (3045 + 3047 + 3048) kol. 3 ≤ AOP-a (3046 + 3049) kol. 3  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30072
        if( aop(iotg,3050,4) == 0 ):
            if not( suma_liste(iotg,[3045,3047,3048],4) <= suma_liste(iotg,[3046,3049],4) ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 4 = 0, ako je AOP (3045 + 3047 + 3048) kol. 4 ≤ AOP-a (3046 + 3049) kol. 4  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30073
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( aop(iotg,3050,4) == aop(iotg,3047,3) ):
                lzbir =  aop(iotg,3050,4) 
                dzbir =  aop(iotg,3047,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3050 kol. 4 = AOP-u 3047 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30074
        if not( aop(iotg,3050,3) == aop(bs,12,5) ):
            lzbir =  aop(iotg,3050,3) 
            dzbir =  aop(bs,12,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3050 kol. 3 = AOP-u 0012 kol. 5  bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3050 kol. 3 = AOP-u 0012 kol. 5  bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30075
        if not( aop(iotg,3050,4) == aop(bs,12,6) ):
            lzbir =  aop(iotg,3050,4) 
            dzbir =  aop(bs,12,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3050 kol. 4 = AOP-u 0012 kol. 6  bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3050 kol. 4 = AOP-u 0012 kol. 6  bilansa stanja Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        
        #IZVEŠTAJ O PROMENAMA NA KAPITALU - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopk,4020,4026,1) + suma(iopk,4046, 4052, 1) +suma(iopk,4072, 4078, 1) +suma(iopk,4100, 4108, 1) +suma(iopk,4128, 4134, 1) +suma(iopk,4154, 4160, 1) +suma(iopk,4181, 4188, 1) +suma(iopk,4208, 4214, 1) + suma_liste(iopk,[4220,4226],1)  > 0 ):
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='Zbir podataka na oznakama za AOP (4020 do 4026) + (4046 do 4052) + (4072 do 4078) + (4100 do 4108) + (4128 do 4134) + (4154 do 4160) + (4181 do 4188) + (4208 do 4214) + 4220 + 4226 > 0 Izveštaj o promenama na kapitalu, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iopk,4001, 4019, 1) +suma(iopk,4027, 4045, 1) +suma(iopk,4053, 4071, 1) +suma(iopk,4079, 4099, 1) +suma(iopk,4109, 4127, 1) +suma(iopk,4135, 4153, 1) +suma(iopk,4161, 4180, 1) +suma(iopk,4189, 4207, 1) +suma(iopk,4215, 4219, 1) +suma(iopk,4221, 4225, 1)  == 0 ):
                lzbir =  suma(iopk,4001, 4019, 1) +suma(iopk,4027, 4045, 1) +suma(iopk,4053, 4071, 1) +suma(iopk,4079, 4099, 1) +suma(iopk,4109, 4127, 1) +suma(iopk,4135, 4153, 1) +suma(iopk,4161, 4180, 1) +suma(iopk,4189, 4207, 1) +suma(iopk,4215, 4219, 1) +suma(iopk,4221, 4225, 1)  
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4019) + (4027 do 4045) + (4053 do 4071) + (4079 do 4099) + (4109 do 4127) + (4135 do 4153) + (4161 do 4180) + (4189 do 4207) + (4215 do 4219) + (4221 do 4225) = 0 Izveštaj o promenama na kapitalu za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iopk,4001, 4019, 1) +suma(iopk,4027, 4045, 1) +suma(iopk,4053, 4071, 1) +suma(iopk,4079, 4099, 1) +suma(iopk,4109, 4127, 1) +suma(iopk,4135, 4153, 1) +suma(iopk,4161, 4180, 1) +suma(iopk,4189, 4207, 1) +suma(iopk,4215, 4219, 1) +suma(iopk,4221, 4225, 1)  > 0 ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4019) + (4027 do 4045) + (4053 do 4071) + (4079 do 4099) + (4109 do 4127) + (4135 do 4153) + (4161 do 4180) + (4189 do 4207) + (4215 do 4219) + (4221 do 4225) > 0 Izveštaj o promenama na kapitalu, po pravilu, mora imati iskazane podatke za prethodni izveštajni period;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40004
        if not( aop(iopk,4006,1) == suma_liste(iopk,[4001,4002,4004],1)-suma_liste(iopk,[4003,4005],1) ):
            lzbir =  aop(iopk,4006,1) 
            dzbir =  suma_liste(iopk,[4001,4002,4004],1)-suma_liste(iopk,[4003,4005],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4006 = AOP-u (4001 + 4002 - 4003 + 4004 - 4005)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40005
        if not( aop(iopk,4032,1) == suma_liste(iopk,[4027,4028,4030],1)-suma_liste(iopk,[4029,4031],1) ):
            lzbir =  aop(iopk,4032,1) 
            dzbir =  suma_liste(iopk,[4027,4028,4030],1)-suma_liste(iopk,[4029,4031],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4032 = AOP-u (4027 + 4028 - 4029 + 4030 - 4031)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40006
        if not( aop(iopk,4058,1) == suma_liste(iopk,[4053,4054,4056],1)-suma_liste(iopk,[4055,4057],1) ):
            lzbir =  aop(iopk,4058,1) 
            dzbir =  suma_liste(iopk,[4053,4054,4056],1)-suma_liste(iopk,[4055,4057],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4058 = AOP-u (4053 + 4054 - 4055 + 4056 - 4057)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40007
        if not( aop(iopk,4084,1) == suma_liste(iopk,[4079,4080,4082],1)-suma_liste(iopk,[4081,4083],1) ):
            lzbir =  aop(iopk,4084,1) 
            dzbir =  suma_liste(iopk,[4079,4080,4082],1)-suma_liste(iopk,[4081,4083],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4084 = AOP-u (4079 + 4080 - 4081 + 4082 - 4083)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40008
        if not( aop(iopk,4114,1) == suma_liste(iopk,[4109,4110,4112],1)-suma_liste(iopk,[4111,4113],1) ):
            lzbir =  aop(iopk,4114,1) 
            dzbir =  suma_liste(iopk,[4109,4110,4112],1)-suma_liste(iopk,[4111,4113],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4114 = AOP-u (4109 + 4110 - 4111 + 4112 - 4113)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40009
        if not( aop(iopk,4140,1) == suma_liste(iopk,[4135,4136,4138],1)-suma_liste(iopk,[4137,4139],1) ):
            lzbir =  aop(iopk,4140,1) 
            dzbir =  suma_liste(iopk,[4135,4136,4138],1)-suma_liste(iopk,[4137,4139],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4140 = AOP-u (4135 + 4136 - 4137 + 4138 - 4139)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40010
        if not( aop(iopk,4166,1) == suma_liste(iopk,[4161,4162,4164],1)-suma_liste(iopk,[4163,4165],1) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  suma_liste(iopk,[4161,4162,4164],1)-suma_liste(iopk,[4163,4165],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u (4161 + 4162 - 4163 + 4164 - 4165)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40011
        if not( aop(iopk,4194,1) == suma_liste(iopk,[4189,4190,4192],1)-suma_liste(iopk,[4191,4193],1) ):
            lzbir =  aop(iopk,4194,1) 
            dzbir =  suma_liste(iopk,[4189,4190,4192],1)-suma_liste(iopk,[4191,4193],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4194 = AOP-u (4189 + 4190 - 4191 + 4192 - 4193)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40012
        if( aop(iopk,4215,1) == suma_liste(iopk,[4001,4053,4079,4109,4161],1)-suma_liste(iopk,[4027,4135,4189],1) ):
            if not( suma_liste(iopk,[4001,4053,4079,4109,4161],1) > suma_liste(iopk,[4027,4135,4189],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4215 = AOP-u (4001 - 4027 + 4053 + 4079 + 4109 - 4135 + 4161 - 4189), ako je AOP (4001 + 4053 + 4079 + 4109 + 4161) > AOP-a  (4027 + 4135 + 4189)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40013
        if( aop(iopk,4221,1) == suma_liste(iopk,[4027,4135,4189],1)-suma_liste(iopk,[4001,4053,4079,4109,4161],1) ):
            if not( suma_liste(iopk,[4001,4053,4079,4109,4161],1) < suma_liste(iopk,[4027,4135,4189],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4221 = AOP-u (4027 - 4001 - 4053 - 4079 - 4109 + 4135 - 4161 + 4189), ako je AOP (4001 + 4053 + 4079 + 4109 + 4161) < AOP-a  (4027 + 4135 + 4189)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40014
        if( aop(iopk,4215,1) + aop(iopk,4221,1) == 0 ):
            if not( suma_liste(iopk,[4001,4053,4079,4109,4161],1) == suma_liste(iopk,[4027,4135,4189],1) ):
                lzbir =  suma_liste(iopk,[4001,4053,4079,4109,4161],1) 
                dzbir =  suma_liste(iopk,[4027,4135,4189],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4215 + 4221) = 0, ako je AOP (4001 + 4053 + 4079 + 4109 + 4161) = AOP-u  (4027 + 4135 + 4189) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40015
        if( aop(iopk,4215,1) > 0 ):
            if not( aop(iopk,4221,1) == 0 ):
                lzbir =  aop(iopk,4221,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4215 > 0 onda je AOP 4221 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40016
        if( aop(iopk,4221,1) > 0 ):
            if not( aop(iopk,4215,1) == 0 ):
                lzbir =  aop(iopk,4215,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4221 > 0 onda je AOP 4215 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40017
        if( aop(iopk,4216,1) == suma_liste(iopk,[4006,4058,4084,4114,4166],1)-suma_liste(iopk,[4032,4140,4194],1) ):
            if not( suma_liste(iopk,[4006,4058,4084,4114,4166],1) > suma_liste(iopk,[4032,4140,4194],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4216 = AOP-u (4006 - 4032 + 4058 + 4084 + 4114 - 4140 + 4166 - 4194), ako je AOP (4006 + 4058 + 4084 + 4114 + 4166) > AOP-a  (4032 + 4140 + 4194)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40018
        if( aop(iopk,4222,1) == suma_liste(iopk,[4032,4140,4194],1)-suma_liste(iopk,[4006,4058,4084,4114,4166],1) ):
            if not( suma_liste(iopk,[4006,4058,4084,4114,4166],1) < suma_liste(iopk,[4032,4140,4194],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4222 = AOP-u (4032 - 4006 - 4058 - 4084 - 4114 + 4140 - 4166 + 4194), ako je AOP (4006 + 4058 + 4084 + 4114 + 4166) < AOP-a  (4032 + 4140 + 4194)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40019
        if( aop(iopk,4216,1) + aop(iopk,4222,1) == 0 ):
            if not( suma_liste(iopk,[4006,4058,4084,4114,4166],1) == suma_liste(iopk,[4032,4140,4194],1) ):
                lzbir =  suma_liste(iopk,[4006,4058,4084,4114,4166],1) 
                dzbir =  suma_liste(iopk,[4032,4140,4194],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4216 + 4222) = 0, ako je AOP (4006 + 4058 + 4084 + 4114 + 4166) = AOP-u  (4032 + 4140 + 4194) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40020
        if( aop(iopk,4216,1) > 0 ):
            if not( aop(iopk,4222,1) == 0 ):
                lzbir =  aop(iopk,4222,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4216 > 0 onda je AOP 4222 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40021
        if( aop(iopk,4222,1) > 0 ):
            if not( aop(iopk,4216,1) == 0 ):
                lzbir =  aop(iopk,4216,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4222 > 0 onda je AOP 4216 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40022
        if not( aop(iopk,4013,1) == suma_liste(iopk,[4006,4007,4009,4011],1)-suma_liste(iopk,[4008,4010,4012],1) ):
            lzbir =  aop(iopk,4013,1) 
            dzbir =  suma_liste(iopk,[4006,4007,4009,4011],1)-suma_liste(iopk,[4008,4010,4012],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4013 = AOP-u (4006 + 4007 - 4008 + 4009 - 4010 + 4011 - 4012)   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40023
        if not( aop(iopk,4039,1) == suma_liste(iopk,[4032,4033,4035,4037],1)-suma_liste(iopk,[4034,4036,4038],1) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  suma_liste(iopk,[4032,4033,4035,4037],1)-suma_liste(iopk,[4034,4036,4038],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u (4032 + 4033 - 4034 + 4035 - 4036 + 4037 - 4038)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40024
        if not( aop(iopk,4065,1) == suma_liste(iopk,[4058,4059,4061,4063],1)-suma_liste(iopk,[4060,4062,4064],1) ):
            lzbir =  aop(iopk,4065,1) 
            dzbir =  suma_liste(iopk,[4058,4059,4061,4063],1)-suma_liste(iopk,[4060,4062,4064],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4065 = AOP-u (4058 + 4059 - 4060 + 4061 - 4062 + 4063 - 4064)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40025
        if not( aop(iopk,4093,1) == suma_liste(iopk,[4084,4086,4088,4091],1)-suma_liste(iopk,[4085,4087,4089,4090,4092],1) ):
            lzbir =  aop(iopk,4093,1) 
            dzbir =  suma_liste(iopk,[4084,4086,4088,4091],1)-suma_liste(iopk,[4085,4087,4089,4090,4092],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4093 = AOP-u (4084 - 4085 + 4086 - 4087 + 4088 - 4089 - 4090 + 4091 - 4092)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40026
        if not( aop(iopk,4121,1) == suma_liste(iopk,[4114,4115,4117,4119],1)-suma_liste(iopk,[4116,4118,4120],1) ):
            lzbir =  aop(iopk,4121,1) 
            dzbir =  suma_liste(iopk,[4114,4115,4117,4119],1)-suma_liste(iopk,[4116,4118,4120],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4121 = AOP-u (4114 + 4115 - 4116 + 4117 - 4118 + 4119 - 4120)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40027
        if not( aop(iopk,4147,1) == suma_liste(iopk,[4140,4142,4143,4145],1)-suma_liste(iopk,[4141,4144,4146],1) ):
            lzbir =  aop(iopk,4147,1) 
            dzbir =  suma_liste(iopk,[4140,4142,4143,4145],1)-suma_liste(iopk,[4141,4144,4146],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4147 = AOP-u (4140 - 4141 + 4142 + 4143 - 4144 + 4145 - 4146)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40028
        if not( aop(iopk,4174,1) == suma_liste(iopk,[4166,4167,4168,4172],1)-suma_liste(iopk,[4169,4170,4171,4173],1) ):
            lzbir =  aop(iopk,4174,1) 
            dzbir =  suma_liste(iopk,[4166,4167,4168,4172],1)-suma_liste(iopk,[4169,4170,4171,4173],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4174 = AOP-u (4166 + 4167 + 4168 - 4169 - 4170 - 4171 + 4172 - 4173)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40029
        if not( aop(iopk,4201,1) == suma_liste(iopk,[4194,4195,4196,4199],1)-suma_liste(iopk,[4197,4198,4200],1) ):
            lzbir =  aop(iopk,4201,1) 
            dzbir =  suma_liste(iopk,[4194,4195,4196,4199],1)-suma_liste(iopk,[4197,4198,4200],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4201 = AOP-u (4194 + 4195 + 4196 - 4197 - 4198 + 4199 - 4200)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40030
        if( aop(iopk,4217,1) == suma_liste(iopk,[4013,4065,4093,4121,4174],1)-suma_liste(iopk,[4039,4147,4201],1) ):
            if not( suma_liste(iopk,[4013,4065,4093,4121,4174],1) > suma_liste(iopk,[4039,4147,4201],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4217 = AOP-u (4013 - 4039 + 4065 + 4093 + 4121 - 4147 + 4174 - 4201), ako je AOP (4013 + 4065 + 4093 + 4121 + 4174) > AOP-a  (4039 + 4147 + 4201)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40031
        if( aop(iopk,4223,1) == suma_liste(iopk,[4039,4147,4201],1)-suma_liste(iopk,[4013,4065,4093,4121,4174],1) ):
            if not( suma_liste(iopk,[4013,4065,4093,4121,4174],1) < suma_liste(iopk,[4039,4147,4201],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4223 = AOP-u (4039 - 4013 - 4065 - 4093 - 4121 + 4147 - 4174 + 4201), ako je AOP (4013 + 4065 + 4093 + 4121 + 4174) < AOP-a (4039 + 4147 + 4201)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40032
        if( aop(iopk,4217,1) + aop(iopk,4223,1) == 0 ):
            if not( suma_liste(iopk,[4013,4065,4093,4121,4174],1) == suma_liste(iopk,[4039,4147,4201],1) ):
                lzbir =  suma_liste(iopk,[4013,4065,4093,4121,4174],1) 
                dzbir =  suma_liste(iopk,[4039,4147,4201],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4217 + 4223) = 0, ako je AOP (4013 + 4065 + 4093 + 4121 + 4174) = AOP-u (4039 + 4147 + 4201) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40033
        if( aop(iopk,4217,1) > 0 ):
            if not( aop(iopk,4223,1) == 0 ):
                lzbir =  aop(iopk,4223,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4217 > 0 onda je AOP 4223 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40034
        if( aop(iopk,4223,1) > 0 ):
            if not( aop(iopk,4217,1) == 0 ):
                lzbir =  aop(iopk,4217,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4223 > 0 onda je AOP 4217 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40035
        if not( aop(iopk,4014,1) == aop(iopk,4013,1) ):
            lzbir =  aop(iopk,4014,1) 
            dzbir =  aop(iopk,4013,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4014 = AOP-u 4013  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40036
        if not( aop(iopk,4040,1) == aop(iopk,4039,1) ):
            lzbir =  aop(iopk,4040,1) 
            dzbir =  aop(iopk,4039,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4040 = AOP-u 4039  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40037
        if not( aop(iopk,4066,1) == aop(iopk,4065,1) ):
            lzbir =  aop(iopk,4066,1) 
            dzbir =  aop(iopk,4065,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4066 = AOP-u 4065  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40038
        if not( aop(iopk,4094,1) == aop(iopk,4093,1) ):
            lzbir =  aop(iopk,4094,1) 
            dzbir =  aop(iopk,4093,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4094 = AOP-u 4093  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40039
        if not( aop(iopk,4122,1) == aop(iopk,4121,1) ):
            lzbir =  aop(iopk,4122,1) 
            dzbir =  aop(iopk,4121,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4122 = AOP-u 4121  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40040
        if not( aop(iopk,4148,1) == aop(iopk,4147,1) ):
            lzbir =  aop(iopk,4148,1) 
            dzbir =  aop(iopk,4147,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4148 = AOP-u 4147  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40041
        if not( aop(iopk,4175,1) == aop(iopk,4174,1) ):
            lzbir =  aop(iopk,4175,1) 
            dzbir =  aop(iopk,4174,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4175 = AOP-u 4174  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40042
        if not( aop(iopk,4202,1) == aop(iopk,4201,1) ):
            lzbir =  aop(iopk,4202,1) 
            dzbir =  aop(iopk,4201,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4202 = AOP-u 4201  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40043
        if not( aop(iopk,4218,1) == aop(iopk,4217,1) ):
            lzbir =  aop(iopk,4218,1) 
            dzbir =  aop(iopk,4217,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4218 = AOP-u 4217  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40044
        if not( aop(iopk,4224,1) == aop(iopk,4223,1) ):
            lzbir =  aop(iopk,4224,1) 
            dzbir =  aop(iopk,4223,1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4224 = AOP-u 4223  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40045
        if not( aop(iopk,4019,1) == suma_liste(iopk,[4014,4015,4017],1)-suma_liste(iopk,[4016,4018],1) ):
            lzbir =  aop(iopk,4019,1) 
            dzbir =  suma_liste(iopk,[4014,4015,4017],1)-suma_liste(iopk,[4016,4018],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4019 = AOP-u (4014 + 4015 - 4016 + 4017 - 4018)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40046
        if not( aop(iopk,4045,1) == suma_liste(iopk,[4040,4041,4043],1)-suma_liste(iopk,[4042,4044],1) ):
            lzbir =  aop(iopk,4045,1) 
            dzbir =  suma_liste(iopk,[4040,4041,4043],1)-suma_liste(iopk,[4042,4044],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4045 = AOP-u (4040 + 4041 - 4042 + 4043 - 4044)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40047
        if not( aop(iopk,4071,1) == suma_liste(iopk,[4066,4067,4069],1)-suma_liste(iopk,[4068,4070],1) ):
            lzbir =  aop(iopk,4071,1) 
            dzbir =  suma_liste(iopk,[4066,4067,4069],1)-suma_liste(iopk,[4068,4070],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4071 = AOP-u (4066 + 4067 - 4068 + 4069 - 4070)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40048
        if not( aop(iopk,4099,1) == suma_liste(iopk,[4094,4095,4097],1)-suma_liste(iopk,[4096,4098],1) ):
            lzbir =  aop(iopk,4099,1) 
            dzbir =  suma_liste(iopk,[4094,4095,4097],1)-suma_liste(iopk,[4096,4098],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4099 = AOP-u (4094 + 4095 - 4096 + 4097 - 4098)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40049
        if not( aop(iopk,4127,1) == suma_liste(iopk,[4122,4123,4125],1)-suma_liste(iopk,[4124,4126],1) ):
            lzbir =  aop(iopk,4127,1) 
            dzbir =  suma_liste(iopk,[4122,4123,4125],1)-suma_liste(iopk,[4124,4126],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4127 = AOP-u (4122 + 4123 - 4124 + 4125 - 4126)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40050
        if not( aop(iopk,4153,1) == suma_liste(iopk,[4148,4149,4151],1)-suma_liste(iopk,[4150,4152],1) ):
            lzbir =  aop(iopk,4153,1) 
            dzbir =  suma_liste(iopk,[4148,4149,4151],1)-suma_liste(iopk,[4150,4152],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4153 = AOP-u (4148 + 4149 - 4150 + 4151 - 4152)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40051
        if not( aop(iopk,4180,1) == suma_liste(iopk,[4175,4176,4178],1)-suma_liste(iopk,[4177,4179],1) ):
            lzbir =  aop(iopk,4180,1) 
            dzbir =  suma_liste(iopk,[4175,4176,4178],1)-suma_liste(iopk,[4177,4179],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4180 = AOP-u (4175 + 4176 - 4177 + 4178 - 4179)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40052
        if not( aop(iopk,4207,1) == suma_liste(iopk,[4202,4203,4205],1)-suma_liste(iopk,[4204,4206],1) ):
            lzbir =  aop(iopk,4207,1) 
            dzbir =  suma_liste(iopk,[4202,4203,4205],1)-suma_liste(iopk,[4204,4206],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4207 = AOP-u (4202 + 4203 - 4204 + 4205 - 4206)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40053
        if( aop(iopk,4219,1) == suma_liste(iopk,[4019,4071,4099,4127,4180],1)-suma_liste(iopk,[4045,4153,4207],1) ):
            if not( suma_liste(iopk,[4019,4071,4099,4127,4180],1) > suma_liste(iopk,[4045,4153,4207],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4219 = AOP-u (4019 - 4045 + 4071 + 4099 + 4127 - 4153 + 4180 - 4207), ako je AOP (4019 + 4071 + 4099 + 4127 + 4180) > AOP-a  (4045 + 4153 + 4207)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40054
        if( aop(iopk,4225,1) == suma_liste(iopk,[4045,4153,4207],1)-suma_liste(iopk,[4019,4071,4099,4127,4180],1) ):
            if not( suma_liste(iopk,[4019,4071,4099,4127,4180],1) < suma_liste(iopk,[4045,4153,4207],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4225 = AOP-u (4045 - 4019 - 4071 - 4099 - 4127 + 4153 - 4180 + 4207), ako je AOP (4019 + 4071 + 4099 + 4127 + 4180) < AOP-a  (4045 + 4153 + 4207)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40055
        if( aop(iopk,4219,1) + aop(iopk,4225,1) == 0 ):
            if not( suma_liste(iopk,[4019,4071,4099,4127,4180],1) == suma_liste(iopk,[4045,4153,4207],1) ):
                lzbir =  suma_liste(iopk,[4019,4071,4099,4127,4180],1) 
                dzbir =  suma_liste(iopk,[4045,4153,4207],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4219 + 4225) = 0, ako je AOP (4019 + 4071 + 4099 + 4127 + 4180) = AOP-u  (4045 + 4153 + 4207) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40056
        if( aop(iopk,4219,1) > 0 ):
            if not( aop(iopk,4225,1) == 0 ):
                lzbir =  aop(iopk,4225,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4219 > 0 onda je AOP 4225 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40057
        if( aop(iopk,4225,1) > 0 ):
            if not( aop(iopk,4219,1) == 0 ):
                lzbir =  aop(iopk,4219,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4225 > 0 onda je AOP 4219 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40058
        if not( aop(iopk,4026,1) == suma_liste(iopk,[4019,4020,4022,4024],1)-suma_liste(iopk,[4021,4023,4025],1) ):
            lzbir =  aop(iopk,4026,1) 
            dzbir =  suma_liste(iopk,[4019,4020,4022,4024],1)-suma_liste(iopk,[4021,4023,4025],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4026 = AOP-u (4019 + 4020 - 4021 + 4022 - 4023 + 4024 - 4025)   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40059
        if not( aop(iopk,4052,1) == suma_liste(iopk,[4045,4046,4048,4050],1)-suma_liste(iopk,[4047,4049,4051],1) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  suma_liste(iopk,[4045,4046,4048,4050],1)-suma_liste(iopk,[4047,4049,4051],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u (4045 + 4046 - 4047 + 4048 - 4049 + 4050 - 4051)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40060
        if not( aop(iopk,4078,1) == suma_liste(iopk,[4071,4072,4074,4076],1)-suma_liste(iopk,[4073,4075,4077],1) ):
            lzbir =  aop(iopk,4078,1) 
            dzbir =  suma_liste(iopk,[4071,4072,4074,4076],1)-suma_liste(iopk,[4073,4075,4077],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4078 = AOP-u (4071 + 4072 - 4073 + 4074 - 4075 + 4076 - 4077)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40061
        if not( aop(iopk,4108,1) == suma_liste(iopk,[4099,4101,4103,4106],1)-suma_liste(iopk,[4100,4102,4104,4105,4107],1) ):
            lzbir =  aop(iopk,4108,1) 
            dzbir =  suma_liste(iopk,[4099,4101,4103,4106],1)-suma_liste(iopk,[4100,4102,4104,4105,4107],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4108 = AOP-u (4099 - 4100 + 4101 - 4102 + 4103 - 4104 - 4105 + 4106 - 4107)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40062
        if not( aop(iopk,4134,1) == suma_liste(iopk,[4127,4128,4130,4132],1)-suma_liste(iopk,[4129,4131,4133],1) ):
            lzbir =  aop(iopk,4134,1) 
            dzbir =  suma_liste(iopk,[4127,4128,4130,4132],1)-suma_liste(iopk,[4129,4131,4133],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4134 = AOP-u (4127 + 4128 - 4129 + 4130 - 4131 + 4132 - 4133)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40063
        if not( aop(iopk,4160,1) == suma_liste(iopk,[4153,4155,4156,4158],1)-suma_liste(iopk,[4154,4157,4159],1) ):
            lzbir =  aop(iopk,4160,1) 
            dzbir =  suma_liste(iopk,[4153,4155,4156,4158],1)-suma_liste(iopk,[4154,4157,4159],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4160 = AOP-u (4153 - 4154 + 4155 + 4156 - 4157 + 4158 - 4159)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40064
        if not( aop(iopk,4188,1) == suma_liste(iopk,[4180,4181,4182,4186],1)-suma_liste(iopk,[4183,4184,4185,4187],1) ):
            lzbir =  aop(iopk,4188,1) 
            dzbir =  suma_liste(iopk,[4180,4181,4182,4186],1)-suma_liste(iopk,[4183,4184,4185,4187],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4188 = AOP-u (4180 + 4181 + 4182 - 4183 - 4184 - 4185 + 4186 - 4187)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40065
        if not( aop(iopk,4214,1) == suma_liste(iopk,[4207,4208,4209,4212],1)-suma_liste(iopk,[4210,4211,4213],1) ):
            lzbir =  aop(iopk,4214,1) 
            dzbir =  suma_liste(iopk,[4207,4208,4209,4212],1)-suma_liste(iopk,[4210,4211,4213],1) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4214 = AOP-u (4207 + 4208 + 4209 - 4210 - 4211 + 4212 - 4213)  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40066
        if( aop(iopk,4220,1) == suma_liste(iopk,[4026,4078,4108,4134,4188],1)-suma_liste(iopk,[4052,4160,4214],1) ):
            if not( suma_liste(iopk,[4026,4078,4108,4134,4188],1) > suma_liste(iopk,[4052,4160,4214],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4220 = AOP-u (4026 - 4052 + 4078 + 4108 + 4134 - 4160 + 4188 - 4214), ako je AOP (4026 + 4078 + 4108 + 4134 + 4188) > AOP-a  (4052 + 4160 + 4214)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40067
        if( aop(iopk,4226,1) == suma_liste(iopk,[4052,4160,4214],1)-suma_liste(iopk,[4026,4078,4108,4134,4188],1) ):
            if not( suma_liste(iopk,[4026,4078,4108,4134,4188],1) < suma_liste(iopk,[4052,4160,4214],1) ):
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4226 = AOP-u (4052 - 4026 - 4078 - 4108 - 4134 + 4160 - 4188 + 4214), ako je AOP (4026 + 4078 + 4108 + 4134 + 4188) < AOP-a  (4052 + 4160 + 4214)  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40068
        if( aop(iopk,4220,1) + aop(iopk,4226,1) == 0 ):
            if not( suma_liste(iopk,[4026,4078,4108,4134,4188],1) == suma_liste(iopk,[4052,4160,4214],1) ):
                lzbir =  suma_liste(iopk,[4026,4078,4108,4134,4188],1) 
                dzbir =  suma_liste(iopk,[4052,4160,4214],1) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP (4220 + 4226) = 0, ako je AOP (4026 + 4078 + 4108 + 4134 + 4188) = AOP-u  (4052 + 4160 + 4214) Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40069
        if( aop(iopk,4220,1) > 0 ):
            if not( aop(iopk,4226,1) == 0 ):
                lzbir =  aop(iopk,4226,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4220 > 0 onda je AOP 4226 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40070
        if( aop(iopk,4226,1) > 0 ):
            if not( aop(iopk,4220,1) == 0 ):
                lzbir =  aop(iopk,4220,1) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='Ako je AOP 4226 > 0 onda je AOP 4220 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40071
        if not( aop(iopk,4006,1) == aop(bs,401,7) ):
            lzbir =  aop(iopk,4006,1) 
            dzbir =  aop(bs,401,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4006 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4006 = AOP-u 0401 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40072
        if not( aop(iopk,4032,1) == aop(bs,407,7) ):
            lzbir =  aop(iopk,4032,1) 
            dzbir =  aop(bs,407,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4032 = AOP-u 0407 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4032 = AOP-u 0407 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40073
        if not( aop(iopk,4058,1) + aop(iopk,4084,1) == aop(bs,402,7) ):
            lzbir =  aop(iopk,4058,1) + aop(iopk,4084,1) 
            dzbir =  aop(bs,402,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4058 + 4084) = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4058 + 4084) = AOP-u 0402 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40074
        if not( aop(iopk,4114,1) == aop(bs,403,7) ):
            lzbir =  aop(iopk,4114,1) 
            dzbir =  aop(bs,403,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4114 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4114 = AOP-u 0403 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40075
        if not( aop(iopk,4140,1) == aop(bs,404,7) ):
            lzbir =  aop(iopk,4140,1) 
            dzbir =  aop(bs,404,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4140 = AOP-u 0404 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4140 = AOP-u 0404 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40076
        if not( aop(iopk,4166,1) == aop(bs,405,7) ):
            lzbir =  aop(iopk,4166,1) 
            dzbir =  aop(bs,405,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4166 = AOP-u 0405 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4166 = AOP-u 0405 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40077
        if not( aop(iopk,4194,1) == aop(bs,406,7) ):
            lzbir =  aop(iopk,4194,1) 
            dzbir =  aop(bs,406,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4194 = AOP-u 0406 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4194 = AOP-u 0406 kol. 7 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40078
        if( aop(iopk,4216,1) == aop(bs,408,7) ):
            if not( aop(bs,408,7) >= 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4216 = AOP-u 0408 kol. 7 bilansa stanja ako je AOP 0408 kol. 7 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4216 = AOP-u 0408 kol. 7 bilansa stanja ako je AOP 0408 kol. 7 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40079
        if( aop(iopk,4222,1) == aop(bs,408,7) ):
            if not( aop(bs,408,7) < 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4222 = AOP-u 0408 kol. 7 bilansa stanja ako je AOP 0408 kol. 7 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4222 = AOP-u 0408 kol. 7 bilansa stanja ako je AOP 0408 kol. 7 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40080
        if not( aop(iopk,4013,1) == aop(bs,401,6) ):
            lzbir =  aop(iopk,4013,1) 
            dzbir =  aop(bs,401,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4013 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4013 = AOP-u 0401 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40081
        if not( aop(iopk,4039,1) == aop(bs,407,6) ):
            lzbir =  aop(iopk,4039,1) 
            dzbir =  aop(bs,407,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4039 = AOP-u 0407 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4039 = AOP-u 0407 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40082
        if not( aop(iopk,4065,1) + aop(iopk,4093,1) == aop(bs,402,6) ):
            lzbir =  aop(iopk,4065,1) + aop(iopk,4093,1) 
            dzbir =  aop(bs,402,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4065 + 4093) = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4065 + 4093) = AOP-u 0402 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40083
        if not( aop(iopk,4121,1) == aop(bs,403,6) ):
            lzbir =  aop(iopk,4121,1) 
            dzbir =  aop(bs,403,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4121 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4121 = AOP-u 0403 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40084
        if not( aop(iopk,4147,1) == aop(bs,404,6) ):
            lzbir =  aop(iopk,4147,1) 
            dzbir =  aop(bs,404,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4147 = AOP-u 0404 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4147 = AOP-u 0404 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40085
        if not( aop(iopk,4174,1) == aop(bs,405,6) ):
            lzbir =  aop(iopk,4174,1) 
            dzbir =  aop(bs,405,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4174 = AOP-u 0405 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4174 = AOP-u 0405 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40086
        if not( aop(iopk,4201,1) == aop(bs,406,6) ):
            lzbir =  aop(iopk,4201,1) 
            dzbir =  aop(bs,406,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4201 = AOP-u 0406 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4201 = AOP-u 0406 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40087
        if( aop(iopk,4217,1) == aop(bs,408,6) ):
            if not( aop(bs,408,6) >= 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4217 = AOP-u 0408 kol. 6 bilansa stanja ako je AOP 0408 kol. 6 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4217 = AOP-u 0408 kol. 6 bilansa stanja ako je AOP 0408 kol. 6 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40088
        if( aop(iopk,4223,1) == aop(bs,408,6) ):
            if not( aop(bs,408,6) < 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4223 = AOP-u 0408 kol. 6 bilansa stanja ako je AOP 0408 kol. 6 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4223 = AOP-u 0408 kol. 6 bilansa stanja ako je AOP 0408 kol. 6 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40089
        if not( aop(iopk,4026,1) == aop(bs,401,5) ):
            lzbir =  aop(iopk,4026,1) 
            dzbir =  aop(bs,401,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4026 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4026 = AOP-u 0401 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40090
        if not( aop(iopk,4052,1) == aop(bs,407,5) ):
            lzbir =  aop(iopk,4052,1) 
            dzbir =  aop(bs,407,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4052 = AOP-u 0407 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4052 = AOP-u 0407 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40091
        if not( aop(iopk,4078,1) + aop(iopk,4108,1) == aop(bs,402,5) ):
            lzbir =  aop(iopk,4078,1) + aop(iopk,4108,1) 
            dzbir =  aop(bs,402,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP (4078 + 4108) = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP (4078 + 4108) = AOP-u 0402 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40092
        if not( aop(iopk,4134,1) == aop(bs,403,5) ):
            lzbir =  aop(iopk,4134,1) 
            dzbir =  aop(bs,403,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4134 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4134 = AOP-u 0403 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40093
        if not( aop(iopk,4160,1) == aop(bs,404,5) ):
            lzbir =  aop(iopk,4160,1) 
            dzbir =  aop(bs,404,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4160 = AOP-u 0404 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4160 = AOP-u 0404 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40094
        if not( aop(iopk,4188,1) == aop(bs,405,5) ):
            lzbir =  aop(iopk,4188,1) 
            dzbir =  aop(bs,405,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4188 = AOP-u 0405 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4188 = AOP-u 0405 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40095
        if not( aop(iopk,4214,1) == aop(bs,406,5) ):
            lzbir =  aop(iopk,4214,1) 
            dzbir =  aop(bs,406,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4214 = AOP-u 0406 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama na kapitalu'
            poruka  ='AOP 4214 = AOP-u 0406 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40096
        if( aop(iopk,4220,1) == aop(bs,408,5) ):
            if not( aop(bs,408,5) >= 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4220 = AOP-u 0408 kol. 5 bilansa stanja ako je AOP 0408 kol. 5 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4220 = AOP-u 0408 kol. 5 bilansa stanja ako je AOP 0408 kol. 5 bilansa stanja ≥ 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40097
        if( aop(iopk,4226,1) == aop(bs,408,5) ):
            if not( aop(bs,408,5) < 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 4226 = AOP-u 0408 kol. 5 bilansa stanja ako je AOP 0408 kol. 5 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o promenama na kapitalu'
                poruka  ='AOP 4226 = AOP-u 0408 kol. 5 bilansa stanja ako je AOP 0408 kol. 5 bilansa stanja < 0 Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju;  '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #90001
        if not((suma(si,9001,9028,4)+suma(si,9029,9036,3)+aop(si,9037,2) +aop(si,9039,4) +aop(si,9038,2) +aop(si,9040,4) +aop(si,9041,6) +aop(si,9042,6))>0):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (9001 do 9028) kol. 4 + (9029 do 9036) kol. 3 + (9037 do 9042) > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9028,5)+suma(si,9029,9036,4) == 0 ):
                lzbir =  suma(si,9001,9028,5)+suma(si,9029,9036,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9028) kol. 5 + (9029 do 9036) kol. 4 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(si,9001,9028,5)+suma(si,9029,9036,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9028) kol. 5 + (9029 do 9036) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90004
        if not( aop(si,9007,4) >= suma(si,9008,9011,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 4 ≥ AOP-a (9008 + 9009 + 9010 + 9011) kol. 4  Troškovi zakupa zemljišta, premija osiguranja, poreza i doprinosa su deo Troškova materijala, energije i usluga i nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90005
        if not( aop(si,9007,5) >= suma(si,9008,9011,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9007 kol. 5 ≥ AOP-a (9008 + 9009 + 9010 + 9011) kol. 5  Troškovi zakupa zemljišta, premija osiguranja, poreza i doprinosa su deo Troškova materijala, energije i usluga i nematerijalnih troškova '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90006
        if not( aop(si,9012,4) == suma(si,9013,9017,4) ):
            lzbir =  aop(si,9012,4) 
            dzbir =  suma(si,9013,9017,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 4 = AOP-u (9013 + 9014 + 9015 + 9016 + 9017) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90007
        if not( aop(si,9012,5) == suma(si,9013,9017,5) ):
            lzbir =  aop(si,9012,5) 
            dzbir =  suma(si,9013,9017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 5 = AOP-u (9013 + 9014 + 9015 + 9016 + 9017) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90008
        if not( aop(si,9013,4) <= suma(si,9002,9004,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 4 ≤ AOP-a (9002 + 9003 + 9004) kol. 4  Troškovi zarada su, po pravilu, manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90009
        if not( aop(si,9013,5) <= suma(si,9002,9004,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9013 kol. 5 ≤ AOP-a (9002 + 9003 + 9004) kol. 5  Troškovi zarada su, po pravilu, manji ili jednaki obavezama za bruto zarade '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90010
        if not( aop(si,9019,4) <= aop(si,9018,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9019 kol. 4 ≤ AOP-a 9018 kol. 4 Rashodi kamata po kreditima i računima u bankama su deo Rashoda kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90011
        if not( aop(si,9019,5) <= aop(si,9018,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9019 kol. 5 ≤ AOP-a 9018 kol. 5 Rashodi kamata po kreditima i računima u bankama su deo Rashoda kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90012
        if not( aop(si,9022,4) <= aop(si,9021,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 4 ≤ AOP-u 9021 kol. 4 Prihodi od zakupa zemljišta su deo Drugih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90013
        if not( aop(si,9022,5) <= aop(si,9021,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9022 kol. 5 ≤ AOP-u 9021 kol. 5 Prihodi od zakupa zemljišta su deo Drugih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90014
        if not( aop(si,9024,4) <= aop(si,9023,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9024 kol. 4 ≤ AOP-a 9023 kol. 4 Prihodi od kamata po računima i depozitima u bankama su deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90015
        if not( aop(si,9024,5) <= aop(si,9023,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9024 kol. 5 ≤ AOP-a 9023 kol. 5 Prihodi od kamata po računima i depozitima u bankama su deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90016
        if not( aop(si,9028,4) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9028 kol. 4 > 0 Na poziciji Prosečan broj zaposlenih nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90017
        if not( aop(si,9028,4) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9028 kol. 4 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90018
        if not( aop(si,9028,5) <= 50 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9028 kol. 5 ≤ 50 Granične vrednosti date su da bi se izbegle slučajne greške prilikom iskazivanja broja zaposlenih; Zakonski zastupnik svojim potpisom potvrđuje ispravnost prikazanog broja zaposlenih; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90019
        if( aop(si,9028,4) > 0 ):
            if not( suma(si,9002,9004,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9028 kol. 4 > 0, onda je AOP (9002 + 9003 + 9004) kol. 4 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane i obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90020
        if( suma(si,9002,9004,4) > 0 ):
            if not( aop(si,9028,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9002 + 9003 + 9004) kol. 4 > 0, onda je AOP 9028 kol. 4 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90021
        if( aop(si,9028,5) > 0 ):
            if not( suma(si,9002,9004,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9028 kol. 5 > 0, onda je AOP (9002 + 9003 + 9004) kol. 5 > 0 Ukoliko je iskazan prosečan broj zaposlenih, obveznik, po pravilu, mora imati iskazane i obaveze po osnovu bruto zarada; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90022
        if( suma(si,9002,9004,5) > 0 ):
            if not( aop(si,9028,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP (9002 + 9003 + 9004) kol. 5 > 0, onda je AOP 9028 kol. 5 > 0 Ukoliko su iskazane obaveze po osnovu bruto zarada, obveznik, po pravilu, mora imati iskazan prosečan broj zaposlenih; Ukoliko jedan od navedenih podataka nije prikazan, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90023
        if not( aop(si,9006,4) == aop(bu,1028,5) ):
            lzbir =  aop(si,9006,4) 
            dzbir =  aop(bu,1028,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9006 kol. 4 = AOP-u 1028 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 4 = AOP-u 1028 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90024
        if not( aop(si,9006,5) == aop(bu,1028,6) ):
            lzbir =  aop(si,9006,5) 
            dzbir =  aop(bu,1028,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9006 kol. 5 = AOP-u 1028 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9006 kol. 5 = AOP-u 1028 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90025
        if not( aop(si,9012,4) == aop(bu,1027,5) ):
            lzbir =  aop(si,9012,4) 
            dzbir =  aop(bu,1027,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9012 kol. 4 = AOP-u 1027 kol . 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 4 = AOP-u 1027 kol . 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90026
        if not( aop(si,9012,5) == aop(bu,1027,6) ):
            lzbir =  aop(si,9012,5) 
            dzbir =  aop(bu,1027,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9012 kol. 5 = AOP-u 1027 kol . 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 5 = AOP-u 1027 kol . 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90027
        if not( aop(si,9023,4) == aop(bu,1023,5) ):
            lzbir =  aop(si,9023,4) 
            dzbir =  aop(bu,1023,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9023 kol. 4 = AOP-u 1023 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 4 = AOP-u 1023 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90028
        if not( aop(si,9023,5) == aop(bu,1023,6) ):
            lzbir =  aop(si,9023,5) 
            dzbir =  aop(bu,1023,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9023 kol. 5 = AOP-u 1023 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9023 kol. 5 = AOP-u 1023 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90029
        if not( aop(si,9018,4) == aop(bu,1024,5) ):
            lzbir =  aop(si,9018,4) 
            dzbir =  aop(bu,1024,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9018 kol. 4 = AOP-u 1024 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 4 = AOP-u 1024 kol. 5 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90030
        if not( aop(si,9018,5) == aop(bu,1024,6) ):
            lzbir =  aop(si,9018,5) 
            dzbir =  aop(bu,1024,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 9018 kol. 5 = AOP-u 1024 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 5 = AOP-u 1024 kol. 6 bilansa uspeha Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90031
        if not( suma(si,9029,9036,3) == aop(iotg,3012,3) ):
            lzbir =  suma(si,9029,9036,3) 
            dzbir =  aop(iotg,3012,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir AOP-a (9029 do 9036) kol. 3 = AOP-u 3012 kol. 3 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9029 do 9036) kol. 3 = AOP-u 3012 kol. 3 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90032
        if not( suma(si,9029,9036,4) == aop(iotg,3012,4) ):
            lzbir =  suma(si,9029,9036,4) 
            dzbir =  aop(iotg,3012,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir AOP-a (9029 do 9036) kol. 4 = AOP-u 3012 kol. 4 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir AOP-a (9029 do 9036) kol. 4 = AOP-u 3012 kol. 4 izveštaja o tokovima gotovine Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 1 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fia,1,12,5) + suma(fia,401,410,5) + suma(fia,1,12,6) + suma(fia,401,410,6) + suma(fia,1,12,7) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) + suma(fia,3001,3039,3) + suma(fia,3001,3039,4) + suma(fia,4001,4015,5) + suma(fia,4001,4015,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0001 do 0012) kol. 6 + (0001 do 0012) kol. 7 bilansa stanja-izveštaja o neto imovini + (0401 do 0410) kol. 5 + (0401 do 0410) kol. 6 + (0401 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha + (3001 do 3039) kol. 3 + (3001 do 3039) kol. 4 izveštaja o tokovima gotovine + (4001 do 4015) kol. 5 + (4001 do 4015) kol. 6 izveštaja o promenama na neto imovini > 0; Finansijski izveštaj ne sme biti bez podataka;"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fia,1,12,5) + suma(fia,401,410,5) + suma(fia,1,12,6) + suma(fia,401,410,6) + suma(fia,1,12,7) + suma(fia,401,410,7) + suma(fia,1001,1020,5) + suma(fia,1001,1020,6) + suma(fia,3001,3039,3) + suma(fia,3001,3039,4) + suma(fia,4001,4015,5) + suma(fia,4001,4015,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND1----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND1----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00000-3 
            # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
            fiaNapomene = Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme;

            if not(proveriNapomene(fiaNapomene, 1, 12, 4) or proveriNapomene(fiaNapomene, 401, 410, 4) or proveriNapomene(fiaNapomene, 1001, 1020, 4) or proveriNapomene(fiaNapomene, 4001, 4015, 4)):
                hasError = True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="Na AOP-u (0001 do 0012) bilansa stanja-izveštaja o neto imovini + (0401 do 0410) bilansa stanja-izveštaja o neto imovini + (1001 do 1020) bilansa uspeha + (4001 do 4015) izveštaja o promenama na neto imovini u koloni 4 (Napomena) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00001
            if not((suma(fia,1,12,5)+suma(fia,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0401 do 0410) kol 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 5 + (0401 do 0410) kol 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fia,1,12,6)+suma(fia,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fia,1,12,7)+suma(fia,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fia,1,12,6)+suma(fia,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fia,1,12,7)+suma(fia,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fia,12,5)==suma(fia,1,11,5)):
                #AOPi
                lzbir =   aop(fia,12,5)
                dzbir =   suma(fia,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fia,12,6)==suma(fia,1,11,6)):
                #AOPi
                lzbir =   aop(fia,12,6)
                dzbir =   suma(fia,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fia,12,7)==suma(fia,1,11,7)):
                #AOPi
                lzbir =   aop(fia,12,7)
                dzbir =   suma(fia,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fia,404,5)== suma(fia,401,403,5)):
                #AOPi
                lzbir =   aop(fia,404,5)
                dzbir =   suma(fia,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fia,404,6)== suma(fia,401,403,6)):
                #AOPi
                lzbir =   aop(fia,404,6)
                dzbir =   suma(fia,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fia,404,7)==suma(fia,401,403,7)):
                #AOPi
                lzbir =   aop(fia,404,7)
                dzbir =   suma(fia,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fia,410,5)==(suma(fia,405,407,5)-suma(fia,408,409,5))):
                #AOPi
                lzbir =   aop(fia,410,5)
                dzbir =   (suma(fia,405,407,5)-suma(fia,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fia,410,6)==(suma(fia,405,407,6)-suma(fia,408,409,6))):
                #AOPi
                lzbir =   aop(fia,410,6)
                dzbir =   (suma(fia,405,407,6)-suma(fia,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fia,410,7)==(suma(fia,405,407,7)-suma(fia,408,409,7))):
                #AOPi
                lzbir =   aop(fia,410,7)
                dzbir =   (suma(fia,405,407,7)-suma(fia,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fia,410,5)==aop(fia,12,5)-aop(fia,404,5)):
                #AOPi
                lzbir =   aop(fia,410,5)
                dzbir =   aop(fia,12,5)-aop(fia,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fia,410,6)==aop(fia,12,6)-aop(fia,404,6)):
                #AOPi
                lzbir =   aop(fia,410,6)
                dzbir =   aop(fia,12,6)-aop(fia,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fia,410,7) == aop(fia,12,7)-aop(fia,404,7)):
                #AOPi
                lzbir =   aop(fia,410,7) 
                dzbir =    aop(fia,12,7)-aop(fia,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fia,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fia,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0;Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fia,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1001,5)>0):
                if not(aop(fia,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fia,1002,5)>0):
                if not(aop(fia,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1001,6)>0):
                if not(aop(fia,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fia,1002,6)>0):
                if not(aop(fia,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1003,5)>0):
                if not(aop(fia,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fia,1004,5)>0):
                if not(aop(fia,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1003,6)>0):
                if not(aop(fia,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fia,1004,6)>0):
                if not(aop(fia,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1005,5)>0):
                if not(aop(fia,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fia,1006,5)>0):
                if not(aop(fia,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1005,6)>0):
                if not(aop(fia,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fia,1006,6)>0):
                if not(aop(fia,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1007,5)>0):
                if not(aop(fia,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fia,1008,5)>0):
                if not(aop(fia,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1007,6)>0):
                if not(aop(fia,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fia,1008,6)>0):
                if not(aop(fia,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1009,5)>0):
                if not(aop(fia,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fia,1010,5)>0):
                if not(aop(fia,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1009,6)>0):
                if not(aop(fia,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fia,1010,6)>0):
                if not(aop(fia,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1010 kol. 6 > 0, onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani neto dobici i gubici    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fia,1019,5)==(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fia,1019,5)
                    dzbir = (suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fia,1019,6)==(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fia,1019,6)
                    dzbir = (suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fia,1020,5)==(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fia,1020,5)
                    dzbir = (suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fia,1020,6)==(suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fia,1020,6)
                    dzbir = (suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fia,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fia,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fia,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fia,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1019,5)>0):
                if not(aop(fia,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fia,1020,5)>0):
                if not(aop(fia,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,1019,6)>0):
                if not(aop(fia,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fia,1020,6)>0):
                if not(aop(fia,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fia,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fia,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            #30001
            if not(suma(fia,3001,3039,3)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #30002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fia,3001,3039,4)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fia,3001,3039,4)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30004
            if not(aop(fia,3001,3)==suma_liste(fia,[3002,3003,3004,3005,3006,3007,3008],3)):
                #AOPi
                lzbir = aop(fia,3001,3)
                dzbir = suma_liste(fia,[3002,3003,3004,3005,3006,3007,3008],3)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30005
            if not(aop(fia,3001,4)==suma_liste(fia,[3002,3003,3004,3005,3006,3007,3008],4)):
                #AOPi
                lzbir = aop(fia,3001,4)
                dzbir = suma_liste(fia,[3002,3003,3004,3005,3006,3007,3008],4)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30006
            if not(aop(fia,3009,3)==suma_liste(fia,[3010,3011,3012,3013,3014,3015,3016],3)):
                #AOPi
                lzbir = aop(fia,3009,3)
                dzbir = suma_liste(fia,[3010,3011,3012,3013,3014,3015,3016],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3009 kol. 3 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30007
            if not(aop(fia,3009,4)==suma_liste(fia,[3010,3011,3012,3013,3014,3015,3016],4)):
                #AOPi
                lzbir = aop(fia,3009,4)
                dzbir = suma_liste(fia,[3010,3011,3012,3013,3014,3015,3016],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3009 kol. 4 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30008
            if(aop(fia,3001,3)>aop(fia,3009,3)):
                if not(aop(fia,3017,3)==(aop(fia,3001,3)-aop(fia,3009,3))):
                    #AOPi
                    lzbir = aop(fia,3017,3)
                    dzbir = (aop(fia,3001,3)-aop(fia,3009,3))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP 3017 kol. 3 = AOP-u (3001 - 3009) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3009 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30009
            if(aop(fia,3001,4)>aop(fia,3009,4)):
                if not(aop(fia,3017,4)==(aop(fia,3001,4)-aop(fia,3009,4))):
                    #AOPi
                    lzbir = aop(fia,3017,4)
                    dzbir = (aop(fia,3001,4)-aop(fia,3009,4))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3017 kol. 4 = AOP-u (3001 - 3009) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30010
            if(aop(fia,3001,3)<aop(fia,3009,3)):
                if not(aop(fia,3018,3)==(aop(fia,3009,3)-aop(fia,3001,3))):
                    #AOPi
                    lzbir = aop(fia,3018,3)
                    dzbir = (aop(fia,3009,3)-aop(fia,3001,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3018 kol. 3 = AOP-u (3009 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3009 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30011
            if(aop(fia,3001,4)<aop(fia,3009,4)):
                if not(aop(fia,3018,4)==(aop(fia,3009,4)-aop(fia,3001,4))):
                    #AOPi
                    lzbir = aop(fia,3018,4)
                    dzbir = (aop(fia,3009,4)-aop(fia,3001,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3018 kol. 4 = AOP-u (3009 - 3001) kol. 4,ako je AOP 3001 kol. 4 < AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30012
            if(aop(fia,3001,3)==aop(fia,3009,3)):
                if not(suma(fia,3017,3018,3)==0):
                    #AOPi
                    lzbir = suma(fia,3017,3018,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3009 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30013
            if(aop(fia,3001,4)==aop(fia,3009,4)):
                if not(suma(fia,3017,3018,4)==0):
                    #AOPi
                    lzbir = suma(fia,3017,3018,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3009 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                   
            #30014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3017,3)>0):
                if not(aop(fia,3018,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3017 kol. 3 > 0,onda je AOP 3018 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30015
            if(aop(fia,3018,3)>0):
                if not(aop(fia,3017,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3018 kol. 3 > 0,onda je AOP 3017 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3017,4)>0):
                if not(aop(fia,3018,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3017 kol. 4 > 0,onda je AOP 3018 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30017
            if(aop(fia,3018,4)>0):
                if not(aop(fia,3017,4)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3018 kol. 4 > 0,onda je AOP 3017 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30018
            if not(suma_liste(fia,[3001,3018],3)==suma_liste(fia,[3009,3017],3)):
                #AOPi
                lzbir = suma_liste(fia,[3001,3018],3)
                dzbir = suma_liste(fia,[3009,3017],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3001 + 3018) kol. 3 = AOP-u (3009 + 3017) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30019
            if not(suma_liste(fia,[3001,3018],4)==suma_liste(fia,[3009,3017],4)):
                #AOPi
                lzbir = suma_liste(fia,[3001,3018],4)
                dzbir = suma_liste(fia,[3009,3017],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3001 + 3018) kol. 4 = AOP-u (3009 + 3017) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30020
            if not(aop(fia,3019,3)==suma(fia,3020,3023,3)):
                #AOPi
                lzbir = aop(fia,3019,3)
                dzbir = suma(fia,3020,3023,3)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30021
            if not(aop(fia,3019,4)==suma(fia,3020,3023,4)):
                #AOPi
                lzbir = aop(fia,3019,4)
                dzbir = suma(fia,3020,3023,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30022
            if not(aop(fia,3024,3)==suma(fia,3025,3029,3)):
                #AOPi
                lzbir = aop(fia,3024,3)
                dzbir = suma(fia,3025,3029,3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3024 kol. 3 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30023
            if not(aop(fia,3024,4)==suma(fia,3025,3029,4)):
                #AOPi
                lzbir = aop(fia,3024,4)
                dzbir = suma(fia,3025,3029,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3024 kol. 4 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30024
            if(aop(fia,3019,3)>aop(fia,3024,3)):
                if not(aop(fia,3030,3)==(aop(fia,3019,3)-aop(fia,3024,3))):
                    #AOPi
                    lzbir = aop(fia,3030,3)
                    dzbir = (aop(fia,3019,3)-aop(fia,3024,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP 3030 kol. 3 = AOP-u (3019 - 3024) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3024 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30025
            if(aop(fia,3019,4)>aop(fia,3024,4)):
                if not(aop(fia,3030,4)==(aop(fia,3019,4)-aop(fia,3024,4))):
                    #AOPi
                    lzbir = aop(fia,3030,4)
                    dzbir = (aop(fia,3019,4)-aop(fia,3024,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3030 kol. 4 = AOP-u (3019 - 3024) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30026
            if(aop(fia,3019,3)<aop(fia,3024,3)):
                if not(aop(fia,3031,3)==(aop(fia,3024,3)-aop(fia,3019,3))):
                    #AOPi
                    lzbir = aop(fia,3031,3)
                    dzbir = (aop(fia,3024,3)-aop(fia,3019,3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3031 kol. 3 = AOP-u (3024 - 3019) kol. 3, ako je AOP 3019 kol. 3 < AOP-a 3024 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30027
            if(aop(fia,3019,4)<aop(fia,3024,4)):
                if not(aop(fia,3031,4)==(aop(fia,3024,4)-aop(fia,3019,4))):
                    #AOPi
                    lzbir = aop(fia,3031,4)
                    dzbir = (aop(fia,3024,4)-aop(fia,3019,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3031 kol. 4 = AOP-u (3024 - 3019) kol. 4, ako je AOP 3019 kol. 4 < AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30028
            if(aop(fia,3019,3)==aop(fia,3024,3)):
                if not(suma(fia,3030,3031,3)==0):
                    #AOPi
                    lzbir = suma(fia,3030,3031,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3024 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30029
            if(aop(fia,3019,4)==aop(fia,3024,4)):
                if not(suma(fia,3030,3031,4)==0):
                    #AOPi
                    lzbir = suma(fia,3030,3031,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3024 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3030,3)>0):
                if not(aop(fia,3031,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3030 kol. 3 > 0,onda je AOP 3031 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30031
            if(aop(fia,3031,3)>0):
                if not(aop(fia,3030,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3031 kol. 3 > 0,onda je AOP 3030 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3030,4)>0):
                if not(aop(fia,3031,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   Ako je AOP 3030 kol. 4 > 0,onda je AOP 3031 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30033
            if(aop(fia,3031,4)>0):
                if not(aop(fia,3030,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   Ako je AOP 3031 kol. 4 > 0,onda je AOP 3030 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30034
            if not(suma_liste(fia,[3019,3031],3)==suma_liste(fia,[3024,3030],3)):
                #AOPi
                lzbir = suma_liste(fia,[3019,3031],3)
                dzbir = suma_liste(fia,[3024,3030],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3019 + 3031) kol. 3 = AOP-u (3024 + 3030) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30035
            if not(suma_liste(fia,[3019,3031],4)==suma_liste(fia,[3024,3030],4)):
                #AOPi
                lzbir = suma_liste(fia,[3019,3031],4)
                dzbir = suma_liste(fia,[3024,3030],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3019 + 3031) kol. 4 = AOP-u (3024 + 3030) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30036
            if not(aop(fia,3032,3)==suma_liste(fia,[3017,3030],3)):
                #AOPi
                lzbir = aop(fia,3032,3)
                dzbir = suma_liste(fia,[3017,3030],3)
                razlika = lzbir - dzbir     
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3032 kol. 3 = AOP-u (3017 + 3030) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30037
            if not(aop(fia,3032,4)==suma_liste(fia,[3017,3030],4)):
                #AOPi
                lzbir = aop(fia,3032,4)
                dzbir = suma_liste(fia,[3017,3030],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3032 kol. 4 = AOP-u (3017 + 3030) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30038
            if not(aop(fia,3033,3)==suma_liste(fia,[3018,3031],3)):
                #AOPi
                lzbir = aop(fia,3033,3)
                dzbir = suma_liste(fia,[3018,3031],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="   AOP 3033 kol. 3 = AOP-u (3018 + 3031) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30039
            if not(aop(fia,3033,4)==suma_liste(fia,[3018,3031],4)):
                #AOPi
                lzbir = aop(fia,3033,4)
                dzbir = suma_liste(fia,[3018,3031],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="   AOP 3033 kol. 4 = AOP-u (3018 + 3031) kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30040
            if(aop(fia,3032,3)>aop(fia,3033,3)):
                if not(aop(fia,3034,3)==(aop(fia,3032,3)-aop(fia,3033,3))):
                    #AOPi
                    lzbir = aop(fia,3034,3)
                    dzbir = (aop(fia,3032,3)-aop(fia,3033,3))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3034 kol. 3 = AOP-u (3032 - 3033) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30041
            if(aop(fia,3032,4)>aop(fia,3033,4)):
                if not(aop(fia,3034,4)==(aop(fia,3032,4)-aop(fia,3033,4))):
                    #AOPi
                    lzbir = aop(fia,3034,4)
                    dzbir = (aop(fia,3032,4)-aop(fia,3033,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP 3034 kol. 4 = AOP-u (3032 - 3033) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3033 kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30042
            if(aop(fia,3032,3)<aop(fia,3033,3)):
                if not(aop(fia,3035,3)==(aop(fia,3033,3)-aop(fia,3032,3))):
                    #AOPi
                    lzbir = aop(fia,3035,3)
                    dzbir = (aop(fia,3033,3)-aop(fia,3032,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3035 kol. 3 = AOP-u (3033 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30043    
            if(aop(fia,3032,4)<aop(fia,3033,4)):
                if not(aop(fia,3035,4)==(aop(fia,3033,4)-aop(fia,3032,4))):
                    #AOPi
                    lzbir = aop(fia,3035,4)
                    dzbir = (aop(fia,3033,4)-aop(fia,3032,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3035 kol. 4 = AOP-u (3033 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3033 kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30044    
            if(aop(fia,3032,3)==aop(fia,3033,3)):
                if not(suma(fia,3034,3035,3)==0):
                    #AOPi
                    lzbir = suma(fia,3034,3035,3)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (3034 + 3035) kol. 3 = 0, ako je AOP 3032 kol. 3 = AOP-u 3033 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30045    
            if(aop(fia,3032,4)==aop(fia,3033,4)):
                if not(suma(fia,3034,3035,4)==0):
                    #AOPi
                    lzbir = suma(fia,3034,3035,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP (3034 + 3035) kol. 4 = 0, ako je AOP 3032 kol. 4 = AOP-u 3033 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30046 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3034,3)>0):
                if not(aop(fia,3035,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3034 kol. 3 > 0,onda je AOP 3035 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30047    
            if(aop(fia,3035,3)>0):
                if not(aop(fia,3034,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3035 kol. 3 > 0,onda je AOP 3034 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30048 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,3034,4)>0):
                if not(aop(fia,3035,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30049
            if(aop(fia,3035,4)>0):
                if not(aop(fia,3034,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30050
            if not(suma_liste(fia,[3032,3035],3)==suma_liste(fia,[3033,3034],3)):
                #AOPi
                lzbir = suma_liste(fia,[3032,3035],3)
                dzbir = suma_liste(fia,[3033,3034],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3032 + 3035) kol. 3 = AOP-u (3033 + 3034) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30051
            if not(suma_liste(fia,[3032,3035],4)==suma_liste(fia,[3033,3034],4)):
                #AOPi
                lzbir = suma_liste(fia,[3032,3035],4)
                dzbir = suma_liste(fia,[3033,3034],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (3032 + 3035) kol. 4 = AOP-u (3033 + 3034) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30052
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(aop(fia,3036,3)==0):
                    hasWarning=True 
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3036 kol. 3 = 0; Novoosnovana pravna lica po pravilu ne smeju imati prikazan podatak za prethodnu godinu "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                
            #30053
            if(suma_liste(fia,[3034,3036,3037],3)>suma_liste(fia,[3035,3038],3)):
                if not(aop(fia,3039,3)==(suma_liste(fia,[3034,3036,3037],3)-suma_liste(fia,[3035,3038],3))):
                    #AOPi
                    lzbir = aop(fia,3039,3)
                    dzbir = (suma_liste(fia,[3034,3036,3037],3)-suma_liste(fia,[3035,3038],3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP 3039 kol. 3 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 3, ako je AOP (3034 + 3036 + 3037) kol. 3 > AOP-a (3035 + 3038) kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30054
            if(suma_liste(fia,[3034,3036,3037],4)>suma_liste(fia,[3035,3038],4)):
                if not(aop(fia,3039,4)==(suma_liste(fia,[3034,3036,3037],4)-suma_liste(fia,[3035,3038],4))):
                    #AOPi
                    lzbir = aop(fia,3039,4)
                    dzbir = (suma_liste(fia,[3034,3036,3037],4)-suma_liste(fia,[3035,3038],4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="   AOP 3039 kol. 4 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 4, ako je AOP (3034 + 3036 + 3037) kol. 4 > AOP-a (3035 + 3038) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30055
            if(suma_liste(fia,[3034,3036,3037],3)<=suma_liste(fia,[3035,3038],3)):
                if not(aop(fia,3039,3)==0):   
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3039 kol. 3 = 0, ako je AOP (3034 + 3036 + 3037) kol. 3 ≤ AOP-a (3035 + 3038) kol. 3 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30056
            if(suma_liste(fia,[3034,3036,3037],4)<=suma_liste(fia,[3035,3038],4)):
                if not(aop(fia,3039,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 3039 kol. 4 = 0, ako je AOP (3034 + 3036 + 3037) kol. 4 ≤ AOP-a (3035 + 3038) kol. 4 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30057
            if not(aop(fia,3039,4)==aop(fia,3036,3)):
                #AOPi
                lzbir = aop(fia,3039,4)
                dzbir = aop(fia,3036,3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 3036 kol. 3   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30058
            if not(aop(fia,3039,3)==aop(fia,1,5)):
                #AOPi
                lzbir = aop(fia,3039,3)
                dzbir = aop(fia,1,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3039 kol. 3 = AOP-u 0001 kol. 5 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga.     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                
            #30059
            if not(aop(fia,3039,4)==aop(fia,1,6)):
                #AOPi
                lzbir = aop(fia,3039,4)
                dzbir = aop(fia,1,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 0001 kol. 6 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga.     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40001    
            if not(suma(fia,4001,4015,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 5 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #40002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):    
                if not(suma(fia,4001,4015,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 = 0; Izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #40003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):    
                if not(suma(fia,4001,4015,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
            #40004
            if(suma_liste(fia,[4002,4004,4005,4006,4007],5)>suma_liste(fia,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fia,4013,5)==(suma_liste(fia,[4002,4004,4005,4006,4007],5)-suma_liste(fia,[4003,4008,4009,4010,4011,4012],5))):
                    #AOPi
                    lzbir = aop(fia,4013,5)
                    dzbir = (suma_liste(fia,[4002,4004,4005,4006,4007],5)-suma_liste(fia,[4003,4008,4009,4010,4011,4012],5))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 4013 kol. 5 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #40005
            if(suma_liste(fia,[4002,4004,4005,4006,4007],6)>suma_liste(fia,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fia,4013,6)==(suma_liste(fia,[4002,4004,4005,4006,4007],6)-suma_liste(fia,[4003,4008,4009,4010,4011,4012],6))):
                    #AOPi
                    lzbir = aop(fia,4013,6)
                    dzbir = (suma_liste(fia,[4002,4004,4005,4006,4007],6)-suma_liste(fia,[4003,4008,4009,4010,4011,4012],6))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 4013 kol. 6 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40006
            if(suma_liste(fia,[4002,4004,4005,4006,4007],5)<suma_liste(fia,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fia,4014,5)==(suma_liste(fia,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fia,[4002,4004,4005,4006,4007],5))):
                    #AOPi
                    lzbir = aop(fia,4014,5)
                    dzbir = (suma_liste(fia,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fia,[4002,4004,4005,4006,4007],5))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 4014 kol. 5 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40007
            if(suma_liste(fia,[4002,4004,4005,4006,4007],6)<suma_liste(fia,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fia,4014,6)==(suma_liste(fia,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fia,[4002,4004,4005,4006,4007],6))):
                    #AOPi
                    lzbir = aop(fia,4014,6)
                    dzbir = (suma_liste(fia,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fia,[4002,4004,4005,4006,4007],6))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP 4014 kol. 6 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40008
            if(suma_liste(fia,[4002,4004,4005,4006,4007],5) == suma_liste(fia,[4003,4008,4009,4010,4011,4012],5)):
                if not(suma(fia,4013,4014,5)== 0):
                    #AOPi
                    lzbir = suma(fia,4013,4014,5)
                    dzbir =  0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (4013 + 4014) kol. 5 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #40009
            if(suma_liste(fia,[4002,4004,4005,4006,4007],6) == suma_liste(fia,[4003,4008,4009,4010,4011,4012],6)):
                if not(suma(fia,4013,4014,6)== 0):
                    #AOPi
                    lzbir = suma(fia,4013,4014,6)
                    dzbir =  0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    AOP (4013 + 4014) kol. 6 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,4013,5)>0):
                if not(aop(fia,4014,5)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 4013 kol. 5 > 0,onda je AOP 4014 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40011    
            if(aop(fia,4014,5)>0):
                if not(aop(fia,4013,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 4014 kol. 5 > 0,onda je AOP 4013 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fia,4013,6)>0):
                if not(aop(fia,4014,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 4013 kol. 6 > 0,onda je AOP 4014 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40013   
            if(aop(fia,4014,6)>0):
                if not(aop(fia,4013,6)==0):  
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 1'
                    poruka  ="    Ako je AOP 4014 kol. 6 > 0,onda je AOP 4013 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40014
            if not(suma_liste(fia,[4002,4004,4005,4006,4007,4014],5)==suma_liste(fia,[4003,4008,4009,4010,4011,4012,4013],5)):
                #AOPi
                lzbir = suma_liste(fia,[4002,4004,4005,4006,4007,4014],5)
                dzbir = suma_liste(fia,[4003,4008,4009,4010,4011,4012,4013],5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40015
            if not(suma_liste(fia,[4002,4004,4005,4006,4007,4014],6)==suma_liste(fia,[4003,4008,4009,4010,4011,4012,4013],6)):
                #AOPi
                lzbir = suma_liste(fia,[4002,4004,4005,4006,4007,4014],6)
                dzbir = suma_liste(fia,[4003,4008,4009,4010,4011,4012,4013],6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže;  Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40016
            if not(aop(fia,4015,5)==(suma_liste(fia,[4001,4013],5)-aop(fia,4014,5))):
                #AOPi
                lzbir = aop(fia,4015,5)
                dzbir = (suma_liste(fia,[4001,4013],5)-aop(fia,4014,5))
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4015 kol. 5 = AOP-u (4001 + 4013 - 4014) kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40017
            if not(aop(fia,4015,6)==(suma_liste(fia,[4001,4013],6)-aop(fia,4014,6))):
                #AOPi
                lzbir = aop(fia,4015,6)
                dzbir = (suma_liste(fia,[4001,4013],6)-aop(fia,4014,6))
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4015 kol. 6 = AOP-u (4001 + 4013 - 4014) kol. 6     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40018
            if not(aop(fia,4015,6)==aop(fia,4001,5)):
                #AOPi
                lzbir = aop(fia,4015,6)
                dzbir = aop(fia,4001,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 4001 kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            
            #40019
            if not(aop(fia,4001,6)==aop(fia,410,7)):
                #AOPi
                lzbir = aop(fia,4001,6)
                dzbir = aop(fia,410,7)
                razlika = lzbir - dzbir
                hasWarning=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4001 kol. 6 = AOP-u 0410 kol. 7 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40020
            if not(aop(fia,4002,5)==aop(fia,406,5)):
                #AOPi
                lzbir = aop(fia,4002,5)
                dzbir = aop(fia,406,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4002 kol. 5 = AOP-u 0406 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40021
            if not(aop(fia,4002,6)==aop(fia,406,6)):
                #AOPi
                lzbir = aop(fia,4002,6)
                dzbir = aop(fia,406,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4002 kol. 6 = AOP-u 0406 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40022
            if not(aop(fia,4003,5)==aop(fia,408,5)):
                #AOPi
                lzbir = aop(fia,4003,5)
                dzbir = aop(fia,408,5)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4003 kol. 5 = AOP-u 0408 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40023
            if not(aop(fia,4003,6)==aop(fia,408,6)):
                #AOPi
                lzbir = aop(fia,4003,6)
                dzbir = aop(fia,408,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4003 kol. 6 = AOP-u 0408 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40024
            if not(aop(fia,4015,5)==aop(fia,410,5)):
                #AOPi
                lzbir = aop(fia,4015,5)
                dzbir = aop(fia,410,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4015 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40025
            if not(aop(fia,4015,6)==aop(fia,410,6)):
                #AOPi
                lzbir = aop(fia,4015,6)
                dzbir = aop(fia,410,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 1'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND1----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND1----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 2 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fib,1,12,5) + suma(fib,401,410,5) + suma(fib,1,12,6) + suma(fib,401,410,6) + suma(fib,1,12,7) + suma(fib,401,410,7) + suma(fib,1001,1020,5) + suma(fib,1001,1020,6) + suma(fib,3001,3039,3) + suma(fib,3001,3039,4) + suma(fib,4001,4015,5) + suma(fib,4001,4015,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 + (0001 do 0410) kol. 6 + (0001 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha + (3001 do 3039) kol. 3 + (3001 do 3039) kol. 4 izveštaja o tokovima gotovine + (4001 do 4015) kol. 5 + (4001 do 4015) kol. 6 izveštaja o promenama na neto imovini > 0; Ukoliko podaci za FOND 1 nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga."
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fib,1,12,5) + suma(fib,401,410,5) + suma(fib,1,12,6) + suma(fib,401,410,6) + suma(fib,1,12,7) + suma(fib,401,410,7) + suma(fib,1001,1020,5) + suma(fib,1001,1020,6) + suma(fib,3001,3039,3) + suma(fib,3001,3039,4) + suma(fib,4001,4015,5) + suma(fib,4001,4015,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND2----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND2----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 2'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00000-3 
            # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
            fibNapomene = Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme;

            if not(proveriNapomene(fibNapomene, 1, 12, 4) or proveriNapomene(fibNapomene, 401, 410, 4) or proveriNapomene(fibNapomene, 1001, 1020, 4) or proveriNapomene(fibNapomene, 4001, 4015, 4)):
                hasError = True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="Na AOP-u (0001 do 0012) bilansa stanja-izveštaja o neto imovini + (0401 do 0410) bilansa stanja-izveštaja o neto imovini + (1001 do 1020) bilansa uspeha + (4001 do 4015) izveštaja o promenama na neto imovini u koloni 4 (Napomena) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00001
            if not((suma(fib,1,12,5)+suma(fib,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fib,1,12,6)+suma(fib,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fib,1,12,7)+suma(fib,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fib,1,12,6)+suma(fib,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fib,1,12,7)+suma(fib,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fib,12,5)==suma(fib,1,11,5)):
                #AOPi
                lzbir =   aop(fib,12,5)
                dzbir =   suma(fib,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fib,12,6)==suma(fib,1,11,6)):
                #AOPi
                lzbir =   aop(fib,12,6)
                dzbir =   suma(fib,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fib,12,7)==suma(fib,1,11,7)):
                #AOPi
                lzbir =   aop(fib,12,7)
                dzbir =   suma(fib,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fib,404,5)== suma(fib,401,403,5)):
                #AOPi
                lzbir =   aop(fib,404,5)
                dzbir =   suma(fib,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fib,404,6)== suma(fib,401,403,6)):
                #AOPi
                lzbir =   aop(fib,404,6)
                dzbir =   suma(fib,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fib,404,7)==suma(fib,401,403,7)):
                #AOPi
                lzbir =   aop(fib,404,7)
                dzbir =   suma(fib,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fib,410,5)==(suma(fib,405,407,5)-suma(fib,408,409,5))):
                #AOPi
                lzbir =   aop(fib,410,5)
                dzbir =   (suma(fib,405,407,5)-suma(fib,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fib,410,6)==(suma(fib,405,407,6)-suma(fib,408,409,6))):
                #AOPi
                lzbir =   aop(fib,410,6)
                dzbir =   (suma(fib,405,407,6)-suma(fib,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fib,410,7)==(suma(fib,405,407,7)-suma(fib,408,409,7))):
                #AOPi
                lzbir =   aop(fib,410,7)
                dzbir =   (suma(fib,405,407,7)-suma(fib,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fib,410,5)==aop(fib,12,5)-aop(fib,404,5)):
                #AOPi
                lzbir =   aop(fib,410,5)
                dzbir =   aop(fib,12,5)-aop(fib,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fib,410,6)==aop(fib,12,6)-aop(fib,404,6)):
                #AOPi
                lzbir =   aop(fib,410,6)
                dzbir =   aop(fib,12,6)-aop(fib,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fib,410,7) == aop(fib,12,7)-aop(fib,404,7)):
                #AOPi
                lzbir =   aop(fib,410,7) 
                dzbir =    aop(fib,12,7)-aop(fib,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fib,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fib,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fib,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1001,5)>0):
                if not(aop(fib,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fib,1002,5)>0):
                if not(aop(fib,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1001,6)>0):
                if not(aop(fib,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fib,1002,6)>0):
                if not(aop(fib,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1003,5)>0):
                if not(aop(fib,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fib,1004,5)>0):
                if not(aop(fib,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1003,6)>0):
                if not(aop(fib,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fib,1004,6)>0):
                if not(aop(fib,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1005,5)>0):
                if not(aop(fib,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fib,1006,5)>0):
                if not(aop(fib,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1005,6)>0):
                if not(aop(fib,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fib,1006,6)>0):
                if not(aop(fib,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1007,5)>0):
                if not(aop(fib,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fib,1008,5)>0):
                if not(aop(fib,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1007,6)>0):
                if not(aop(fib,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fib,1008,6)>0):
                if not(aop(fib,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1009,5)>0):
                if not(aop(fib,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fib,1010,5)>0):
                if not(aop(fib,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1009,6)>0):
                if not(aop(fib,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fib,1010,6)>0):
                if not(aop(fib,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fib,1019,5)==(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fib,1019,5)
                    dzbir = (suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fib,1019,6)==(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fib,1019,6)
                    dzbir = (suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fib,1020,5)==(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fib,1020,5)
                    dzbir = (suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fib,1020,6)==(suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fib,1020,6)
                    dzbir = (suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fib,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fib,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fib,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fib,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1019,5)>0):
                if not(aop(fib,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fib,1020,5)>0):
                if not(aop(fib,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,1019,6)>0):
                if not(aop(fib,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fib,1020,6)>0):
                if not(aop(fib,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fib,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fib,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            #30001
            if not(suma(fib,3001,3039,3)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #30002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fib,3001,3039,4)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fib,3001,3039,4)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30004
            if not(aop(fib,3001,3)==suma_liste(fib,[3002,3003,3004,3005,3006,3007,3008],3)):
                #AOPi
                lzbir = aop(fib,3001,3)
                dzbir = suma_liste(fib,[3002,3003,3004,3005,3006,3007,3008],3)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30005
            if not(aop(fib,3001,4)==suma_liste(fib,[3002,3003,3004,3005,3006,3007,3008],4)):
                #AOPi
                lzbir = aop(fib,3001,4)
                dzbir = suma_liste(fib,[3002,3003,3004,3005,3006,3007,3008],4)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30006
            if not(aop(fib,3009,3)==suma_liste(fib,[3010,3011,3012,3013,3014,3015,3016],3)):
                #AOPi
                lzbir = aop(fib,3009,3)
                dzbir = suma_liste(fib,[3010,3011,3012,3013,3014,3015,3016],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3009 kol. 3 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30007
            if not(aop(fib,3009,4)==suma_liste(fib,[3010,3011,3012,3013,3014,3015,3016],4)):
                #AOPi
                lzbir = aop(fib,3009,4)
                dzbir = suma_liste(fib,[3010,3011,3012,3013,3014,3015,3016],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3009 kol. 4 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30008
            if(aop(fib,3001,3)>aop(fib,3009,3)):
                if not(aop(fib,3017,3)==(aop(fib,3001,3)-aop(fib,3009,3))):
                    #AOPi
                    lzbir = aop(fib,3017,3)
                    dzbir = (aop(fib,3001,3)-aop(fib,3009,3))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP 3017 kol. 3 = AOP-u (3001 - 3009) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3009 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30009
            if(aop(fib,3001,4)>aop(fib,3009,4)):
                if not(aop(fib,3017,4)==(aop(fib,3001,4)-aop(fib,3009,4))):
                    #AOPi
                    lzbir = aop(fib,3017,4)
                    dzbir = (aop(fib,3001,4)-aop(fib,3009,4))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3017 kol. 4 = AOP-u (3001 - 3009) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30010
            if(aop(fib,3001,3)<aop(fib,3009,3)):
                if not(aop(fib,3018,3)==(aop(fib,3009,3)-aop(fib,3001,3))):
                    #AOPi
                    lzbir = aop(fib,3018,3)
                    dzbir = (aop(fib,3009,3)-aop(fib,3001,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3018 kol. 3 = AOP-u (3009 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3009 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30011
            if(aop(fib,3001,4)<aop(fib,3009,4)):
                if not(aop(fib,3018,4)==(aop(fib,3009,4)-aop(fib,3001,4))):
                    #AOPi
                    lzbir = aop(fib,3018,4)
                    dzbir = (aop(fib,3009,4)-aop(fib,3001,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3018 kol. 4 = AOP-u (3009 - 3001) kol. 4,ako je AOP 3001 kol. 4 < AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30012
            if(aop(fib,3001,3)==aop(fib,3009,3)):
                if not(suma(fib,3017,3018,3)==0):
                    #AOPi
                    lzbir = suma(fib,3017,3018,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3009 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30013
            if(aop(fib,3001,4)==aop(fib,3009,4)):
                if not(suma(fib,3017,3018,4)==0):
                    #AOPi
                    lzbir = suma(fib,3017,3018,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3009 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                   
            #30014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3017,3)>0):
                if not(aop(fib,3018,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3017 kol. 3 > 0,onda je AOP 3018 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30015
            if(aop(fib,3018,3)>0):
                if not(aop(fib,3017,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3018 kol. 3 > 0,onda je AOP 3017 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3017,4)>0):
                if not(aop(fib,3018,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3017 kol. 4 > 0,onda je AOP 3018 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30017
            if(aop(fib,3018,4)>0):
                if not(aop(fib,3017,4)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3018 kol. 4 > 0,onda je AOP 3017 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30018
            if not(suma_liste(fib,[3001,3018],3)==suma_liste(fib,[3009,3017],3)):
                #AOPi
                lzbir = suma_liste(fib,[3001,3018],3)
                dzbir = suma_liste(fib,[3009,3017],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3001 + 3018) kol. 3 = AOP-u (3009 + 3017) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30019
            if not(suma_liste(fib,[3001,3018],4)==suma_liste(fib,[3009,3017],4)):
                #AOPi
                lzbir = suma_liste(fib,[3001,3018],4)
                dzbir = suma_liste(fib,[3009,3017],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3001 + 3018) kol. 4 = AOP-u (3009 + 3017) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30020
            if not(aop(fib,3019,3)==suma(fib,3020,3023,3)):
                #AOPi
                lzbir = aop(fib,3019,3)
                dzbir = suma(fib,3020,3023,3)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30021
            if not(aop(fib,3019,4)==suma(fib,3020,3023,4)):
                #AOPi
                lzbir = aop(fib,3019,4)
                dzbir = suma(fib,3020,3023,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30022
            if not(aop(fib,3024,3)==suma(fib,3025,3029,3)):
                #AOPi
                lzbir = aop(fib,3024,3)
                dzbir = suma(fib,3025,3029,3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3024 kol. 3 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30023
            if not(aop(fib,3024,4)==suma(fib,3025,3029,4)):
                #AOPi
                lzbir = aop(fib,3024,4)
                dzbir = suma(fib,3025,3029,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3024 kol. 4 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30024
            if(aop(fib,3019,3)>aop(fib,3024,3)):
                if not(aop(fib,3030,3)==(aop(fib,3019,3)-aop(fib,3024,3))):
                    #AOPi
                    lzbir = aop(fib,3030,3)
                    dzbir = (aop(fib,3019,3)-aop(fib,3024,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP 3030 kol. 3 = AOP-u (3019 - 3024) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3024 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30025
            if(aop(fib,3019,4)>aop(fib,3024,4)):
                if not(aop(fib,3030,4)==(aop(fib,3019,4)-aop(fib,3024,4))):
                    #AOPi
                    lzbir = aop(fib,3030,4)
                    dzbir = (aop(fib,3019,4)-aop(fib,3024,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3030 kol. 4 = AOP-u (3019 - 3024) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30026
            if(aop(fib,3019,3)<aop(fib,3024,3)):
                if not(aop(fib,3031,3)==(aop(fib,3024,3)-aop(fib,3019,3))):
                    #AOPi
                    lzbir = aop(fib,3031,3)
                    dzbir = (aop(fib,3024,3)-aop(fib,3019,3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3031 kol. 3 = AOP-u (3024 - 3019) kol. 3, ako je AOP 3019 kol. 3 < AOP-a 3024 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30027
            if(aop(fib,3019,4)<aop(fib,3024,4)):
                if not(aop(fib,3031,4)==(aop(fib,3024,4)-aop(fib,3019,4))):
                    #AOPi
                    lzbir = aop(fib,3031,4)
                    dzbir = (aop(fib,3024,4)-aop(fib,3019,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3031 kol. 4 = AOP-u (3024 - 3019) kol. 4, ako je AOP 3019 kol. 4 < AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30028
            if(aop(fib,3019,3)==aop(fib,3024,3)):
                if not(suma(fib,3030,3031,3)==0):
                    #AOPi
                    lzbir = suma(fib,3030,3031,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3024 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30029
            if(aop(fib,3019,4)==aop(fib,3024,4)):
                if not(suma(fib,3030,3031,4)==0):
                    #AOPi
                    lzbir = suma(fib,3030,3031,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3024 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3030,3)>0):
                if not(aop(fib,3031,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3030 kol. 3 > 0,onda je AOP 3031 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30031
            if(aop(fib,3031,3)>0):
                if not(aop(fib,3030,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3031 kol. 3 > 0,onda je AOP 3030 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3030,4)>0):
                if not(aop(fib,3031,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   Ako je AOP 3030 kol. 4 > 0,onda je AOP 3031 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30033
            if(aop(fib,3031,4)>0):
                if not(aop(fib,3030,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   Ako je AOP 3031 kol. 4 > 0,onda je AOP 3030 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30034
            if not(suma_liste(fib,[3019,3031],3)==suma_liste(fib,[3024,3030],3)):
                #AOPi
                lzbir = suma_liste(fib,[3019,3031],3)
                dzbir = suma_liste(fib,[3024,3030],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3019 + 3031) kol. 3 = AOP-u (3024 + 3030) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30035
            if not(suma_liste(fib,[3019,3031],4)==suma_liste(fib,[3024,3030],4)):
                #AOPi
                lzbir = suma_liste(fib,[3019,3031],4)
                dzbir = suma_liste(fib,[3024,3030],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3019 + 3031) kol. 4 = AOP-u (3024 + 3030) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30036
            if not(aop(fib,3032,3)==suma_liste(fib,[3017,3030],3)):
                #AOPi
                lzbir = aop(fib,3032,3)
                dzbir = suma_liste(fib,[3017,3030],3)
                razlika = lzbir - dzbir     
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3032 kol. 3 = AOP-u (3017 + 3030) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30037
            if not(aop(fib,3032,4)==suma_liste(fib,[3017,3030],4)):
                #AOPi
                lzbir = aop(fib,3032,4)
                dzbir = suma_liste(fib,[3017,3030],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3032 kol. 4 = AOP-u (3017 + 3030) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30038
            if not(aop(fib,3033,3)==suma_liste(fib,[3018,3031],3)):
                #AOPi
                lzbir = aop(fib,3033,3)
                dzbir = suma_liste(fib,[3018,3031],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="   AOP 3033 kol. 3 = AOP-u (3018 + 3031) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30039
            if not(aop(fib,3033,4)==suma_liste(fib,[3018,3031],4)):
                #AOPi
                lzbir = aop(fib,3033,4)
                dzbir = suma_liste(fib,[3018,3031],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="   AOP 3033 kol. 4 = AOP-u (3018 + 3031) kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30040
            if(aop(fib,3032,3)>aop(fib,3033,3)):
                if not(aop(fib,3034,3)==(aop(fib,3032,3)-aop(fib,3033,3))):
                    #AOPi
                    lzbir = aop(fib,3034,3)
                    dzbir = (aop(fib,3032,3)-aop(fib,3033,3))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3034 kol. 3 = AOP-u (3032 - 3033) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30041
            if(aop(fib,3032,4)>aop(fib,3033,4)):
                if not(aop(fib,3034,4)==(aop(fib,3032,4)-aop(fib,3033,4))):
                    #AOPi
                    lzbir = aop(fib,3034,4)
                    dzbir = (aop(fib,3032,4)-aop(fib,3033,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP 3034 kol. 4 = AOP-u (3032 - 3033) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3033 kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30042
            if(aop(fib,3032,3)<aop(fib,3033,3)):
                if not(aop(fib,3035,3)==(aop(fib,3033,3)-aop(fib,3032,3))):
                    #AOPi
                    lzbir = aop(fib,3035,3)
                    dzbir = (aop(fib,3033,3)-aop(fib,3032,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3035 kol. 3 = AOP-u (3033 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30043    
            if(aop(fib,3032,4)<aop(fib,3033,4)):
                if not(aop(fib,3035,4)==(aop(fib,3033,4)-aop(fib,3032,4))):
                    #AOPi
                    lzbir = aop(fib,3035,4)
                    dzbir = (aop(fib,3033,4)-aop(fib,3032,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3035 kol. 4 = AOP-u (3033 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3033 kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30044    
            if(aop(fib,3032,3)==aop(fib,3033,3)):
                if not(suma(fib,3034,3035,3)==0):
                    #AOPi
                    lzbir = suma(fib,3034,3035,3)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (3034 + 3035) kol. 3 = 0, ako je AOP 3032 kol. 3 = AOP-u 3033 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30045    
            if(aop(fib,3032,4)==aop(fib,3033,4)):
                if not(suma(fib,3034,3035,4)==0):
                    #AOPi
                    lzbir = suma(fib,3034,3035,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP (3034 + 3035) kol. 4 = 0, ako je AOP 3032 kol. 4 = AOP-u 3033 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30046 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3034,3)>0):
                if not(aop(fib,3035,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3034 kol. 3 > 0,onda je AOP 3035 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30047    
            if(aop(fib,3035,3)>0):
                if not(aop(fib,3034,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3035 kol. 3 > 0,onda je AOP 3034 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30048 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,3034,4)>0):
                if not(aop(fib,3035,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30049
            if(aop(fib,3035,4)>0):
                if not(aop(fib,3034,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30050
            if not(suma_liste(fib,[3032,3035],3)==suma_liste(fib,[3033,3034],3)):
                #AOPi
                lzbir = suma_liste(fib,[3032,3035],3)
                dzbir = suma_liste(fib,[3033,3034],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3032 + 3035) kol. 3 = AOP-u (3033 + 3034) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30051
            if not(suma_liste(fib,[3032,3035],4)==suma_liste(fib,[3033,3034],4)):
                #AOPi
                lzbir = suma_liste(fib,[3032,3035],4)
                dzbir = suma_liste(fib,[3033,3034],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (3032 + 3035) kol. 4 = AOP-u (3033 + 3034) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30052
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(aop(fib,3036,3)==0):
                    hasWarning=True 
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3036 kol. 3 = 0; Novoosnovana pravna lica po pravilu ne smeju imati prikazan podatak za prethodnu godinu "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                
            #30053
            if(suma_liste(fib,[3034,3036,3037],3)>suma_liste(fib,[3035,3038],3)):
                if not(aop(fib,3039,3)==(suma_liste(fib,[3034,3036,3037],3)-suma_liste(fib,[3035,3038],3))):
                    #AOPi
                    lzbir = aop(fib,3039,3)
                    dzbir = (suma_liste(fib,[3034,3036,3037],3)-suma_liste(fib,[3035,3038],3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP 3039 kol. 3 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 3, ako je AOP (3034 + 3036 + 3037) kol. 3 > AOP-a (3035 + 3038) kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30054
            if(suma_liste(fib,[3034,3036,3037],4)>suma_liste(fib,[3035,3038],4)):
                if not(aop(fib,3039,4)==(suma_liste(fib,[3034,3036,3037],4)-suma_liste(fib,[3035,3038],4))):
                    #AOPi
                    lzbir = aop(fib,3039,4)
                    dzbir = (suma_liste(fib,[3034,3036,3037],4)-suma_liste(fib,[3035,3038],4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="   AOP 3039 kol. 4 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 4, ako je AOP (3034 + 3036 + 3037) kol. 4 > AOP-a (3035 + 3038) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30055
            if(suma_liste(fib,[3034,3036,3037],3)<=suma_liste(fib,[3035,3038],3)):
                if not(aop(fib,3039,3)==0):   
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3039 kol. 3 = 0, ako je AOP (3034 + 3036 + 3037) kol. 3 ≤ AOP-a (3035 + 3038) kol. 3 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30056
            if(suma_liste(fib,[3034,3036,3037],4)<=suma_liste(fib,[3035,3038],4)):
                if not(aop(fib,3039,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 3039 kol. 4 = 0, ako je AOP (3034 + 3036 + 3037) kol. 4 ≤ AOP-a (3035 + 3038) kol. 4 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30057
            if not(aop(fib,3039,4)==aop(fib,3036,3)):
                #AOPi
                lzbir = aop(fib,3039,4)
                dzbir = aop(fib,3036,3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 3036 kol. 3   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30058
            if not(aop(fib,3039,3)==aop(fib,1,5)):
                #AOPi
                lzbir = aop(fib,3039,3)
                dzbir = aop(fib,1,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3039 kol. 3 = AOP-u 0001 kol. 5 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                
            #30059
            if not(aop(fib,3039,4)==aop(fib,1,6)):
                #AOPi
                lzbir = aop(fib,3039,4)
                dzbir = aop(fib,1,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 0001 kol. 6 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40001    
            if not(suma(fib,4001,4015,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 5 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #40002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):    
                if not(suma(fib,4001,4015,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 = 0; Izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #40003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):    
                if not(suma(fib,4001,4015,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
            #40004
            if(suma_liste(fib,[4002,4004,4005,4006,4007],5)>suma_liste(fib,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fib,4013,5)==(suma_liste(fib,[4002,4004,4005,4006,4007],5)-suma_liste(fib,[4003,4008,4009,4010,4011,4012],5))):
                    #AOPi
                    lzbir = aop(fib,4013,5)
                    dzbir = (suma_liste(fib,[4002,4004,4005,4006,4007],5)-suma_liste(fib,[4003,4008,4009,4010,4011,4012],5))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 4013 kol. 5 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #40005
            if(suma_liste(fib,[4002,4004,4005,4006,4007],6)>suma_liste(fib,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fib,4013,6)==(suma_liste(fib,[4002,4004,4005,4006,4007],6)-suma_liste(fib,[4003,4008,4009,4010,4011,4012],6))):
                    #AOPi
                    lzbir = aop(fib,4013,6)
                    dzbir = (suma_liste(fib,[4002,4004,4005,4006,4007],6)-suma_liste(fib,[4003,4008,4009,4010,4011,4012],6))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 4013 kol. 6 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40006
            if(suma_liste(fib,[4002,4004,4005,4006,4007],5)<suma_liste(fib,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fib,4014,5)==(suma_liste(fib,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fib,[4002,4004,4005,4006,4007],5))):
                    #AOPi
                    lzbir = aop(fib,4014,5)
                    dzbir = (suma_liste(fib,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fib,[4002,4004,4005,4006,4007],5))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 4014 kol. 5 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40007
            if(suma_liste(fib,[4002,4004,4005,4006,4007],6)<suma_liste(fib,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fib,4014,6)==(suma_liste(fib,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fib,[4002,4004,4005,4006,4007],6))):
                    #AOPi
                    lzbir = aop(fib,4014,6)
                    dzbir = (suma_liste(fib,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fib,[4002,4004,4005,4006,4007],6))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP 4014 kol. 6 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40008
            if(suma_liste(fib,[4002,4004,4005,4006,4007],5) == suma_liste(fib,[4003,4008,4009,4010,4011,4012],5)):
                if not(suma(fib,4013,4014,5)== 0):
                    #AOPi
                    lzbir = suma(fib,4013,4014,5)
                    dzbir =  0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (4013 + 4014) kol. 5 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #40009
            if(suma_liste(fib,[4002,4004,4005,4006,4007],6) == suma_liste(fib,[4003,4008,4009,4010,4011,4012],6)):
                if not(suma(fib,4013,4014,6)== 0):
                    #AOPi
                    lzbir = suma(fib,4013,4014,6)
                    dzbir =  0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    AOP (4013 + 4014) kol. 6 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,4013,5)>0):
                if not(aop(fib,4014,5)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 4013 kol. 5 > 0,onda je AOP 4014 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40011    
            if(aop(fib,4014,5)>0):
                if not(aop(fib,4013,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 4014 kol. 5 > 0,onda je AOP 4013 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fib,4013,6)>0):
                if not(aop(fib,4014,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 4013 kol. 6 > 0,onda je AOP 4014 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40013   
            if(aop(fib,4014,6)>0):
                if not(aop(fib,4013,6)==0):  
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 2'
                    poruka  ="    Ako je AOP 4014 kol. 6 > 0,onda je AOP 4013 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40014
            if not(suma_liste(fib,[4002,4004,4005,4006,4007,4014],5)==suma_liste(fib,[4003,4008,4009,4010,4011,4012,4013],5)):
                #AOPi
                lzbir = suma_liste(fib,[4002,4004,4005,4006,4007,4014],5)
                dzbir = suma_liste(fib,[4003,4008,4009,4010,4011,4012,4013],5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40015
            if not(suma_liste(fib,[4002,4004,4005,4006,4007,4014],6)==suma_liste(fib,[4003,4008,4009,4010,4011,4012,4013],6)):
                #AOPi
                lzbir = suma_liste(fib,[4002,4004,4005,4006,4007,4014],6)
                dzbir = suma_liste(fib,[4003,4008,4009,4010,4011,4012,4013],6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže;  Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40016
            if not(aop(fib,4015,5)==(suma_liste(fib,[4001,4013],5)-aop(fib,4014,5))):
                #AOPi
                lzbir = aop(fib,4015,5)
                dzbir = (suma_liste(fib,[4001,4013],5)-aop(fib,4014,5))
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4015 kol. 5 = AOP-u (4001 + 4013 - 4014) kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40017
            if not(aop(fib,4015,6)==(suma_liste(fib,[4001,4013],6)-aop(fib,4014,6))):
                #AOPi
                lzbir = aop(fib,4015,6)
                dzbir = (suma_liste(fib,[4001,4013],6)-aop(fib,4014,6))
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4015 kol. 6 = AOP-u (4001 + 4013 - 4014) kol. 6     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40018
            if not(aop(fib,4015,6)==aop(fib,4001,5)):
                #AOPi
                lzbir = aop(fib,4015,6)
                dzbir = aop(fib,4001,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 4001 kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            
            #40019
            if not(aop(fib,4001,6)==aop(fib,410,7)):
                #AOPi
                lzbir = aop(fib,4001,6)
                dzbir = aop(fib,410,7)
                razlika = lzbir - dzbir
                hasWarning=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4001 kol. 6 = AOP-u 0410 kol. 7 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40020
            if not(aop(fib,4002,5)==aop(fib,406,5)):
                #AOPi
                lzbir = aop(fib,4002,5)
                dzbir = aop(fib,406,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4002 kol. 5 = AOP-u 0406 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40021
            if not(aop(fib,4002,6)==aop(fib,406,6)):
                #AOPi
                lzbir = aop(fib,4002,6)
                dzbir = aop(fib,406,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4002 kol. 6 = AOP-u 0406 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40022
            if not(aop(fib,4003,5)==aop(fib,408,5)):
                #AOPi
                lzbir = aop(fib,4003,5)
                dzbir = aop(fib,408,5)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4003 kol. 5 = AOP-u 0408 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40023
            if not(aop(fib,4003,6)==aop(fib,408,6)):
                #AOPi
                lzbir = aop(fib,4003,6)
                dzbir = aop(fib,408,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4003 kol. 6 = AOP-u 0408 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40024
            if not(aop(fib,4015,5)==aop(fib,410,5)):
                #AOPi
                lzbir = aop(fib,4015,5)
                dzbir = aop(fib,410,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4015 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40025
            if not(aop(fib,4015,6)==aop(fib,410,6)):
                #AOPi
                lzbir = aop(fib,4015,6)
                dzbir = aop(fib,410,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 2'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND2----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND2----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 3 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fic,1,12,5) + suma(fic,401,410,5) + suma(fic,1,12,6) + suma(fic,401,410,6) + suma(fic,1,12,7) + suma(fic,401,410,7) + suma(fic,1001,1020,5) + suma(fic,1001,1020,6) + suma(fic,3001,3039,3) + suma(fic,3001,3039,4) + suma(fic,4001,4015,5) + suma(fic,4001,4015,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 + (0001 do 0410) kol. 6 + (0001 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha + (3001 do 3039) kol. 3 + (3001 do 3039) kol. 4 izveštaja o tokovima gotovine + (4001 do 4015) kol. 5 + (4001 do 4015) kol. 6 izveštaja o promenama na neto imovini > 0; Ukoliko podaci za FOND 1 nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga."
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fic,1,12,5) + suma(fic,401,410,5) + suma(fic,1,12,6) + suma(fic,401,410,6) + suma(fic,1,12,7) + suma(fic,401,410,7) + suma(fic,1001,1020,5) + suma(fic,1001,1020,6) + suma(fic,3001,3039,3) + suma(fic,3001,3039,4) + suma(fic,4001,4015,5) + suma(fic,4001,4015,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND3----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND3----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 3'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00000-3 
            # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
            ficNapomene = Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme;

            if not(proveriNapomene(ficNapomene, 1, 12, 4) or proveriNapomene(ficNapomene, 401, 410, 4) or proveriNapomene(ficNapomene, 1001, 1020, 4) or proveriNapomene(ficNapomene, 4001, 4015, 4)):
                hasError = True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="Na AOP-u (0001 do 0012) bilansa stanja-izveštaja o neto imovini + (0401 do 0410) bilansa stanja-izveštaja o neto imovini + (1001 do 1020) bilansa uspeha + (4001 do 4015) izveštaja o promenama na neto imovini u koloni 4 (Napomena) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00001
            if not((suma(fic,1,12,5)+suma(fic,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fic,1,12,6)+suma(fic,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fic,1,12,7)+suma(fic,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fic,1,12,6)+suma(fic,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fic,1,12,7)+suma(fic,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fic,12,5)==suma(fic,1,11,5)):
                #AOPi
                lzbir =   aop(fic,12,5)
                dzbir =   suma(fic,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fic,12,6)==suma(fic,1,11,6)):
                #AOPi
                lzbir =   aop(fic,12,6)
                dzbir =   suma(fic,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fic,12,7)==suma(fic,1,11,7)):
                #AOPi
                lzbir =   aop(fic,12,7)
                dzbir =   suma(fic,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fic,404,5)== suma(fic,401,403,5)):
                #AOPi
                lzbir =   aop(fic,404,5)
                dzbir =   suma(fic,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fic,404,6)== suma(fic,401,403,6)):
                #AOPi
                lzbir =   aop(fic,404,6)
                dzbir =   suma(fic,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fic,404,7)==suma(fic,401,403,7)):
                #AOPi
                lzbir =   aop(fic,404,7)
                dzbir =   suma(fic,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fic,410,5)==(suma(fic,405,407,5)-suma(fic,408,409,5))):
                #AOPi
                lzbir =   aop(fic,410,5)
                dzbir =   (suma(fic,405,407,5)-suma(fic,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fic,410,6)==(suma(fic,405,407,6)-suma(fic,408,409,6))):
                #AOPi
                lzbir =   aop(fic,410,6)
                dzbir =   (suma(fic,405,407,6)-suma(fic,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fic,410,7)==(suma(fic,405,407,7)-suma(fic,408,409,7))):
                #AOPi
                lzbir =   aop(fic,410,7)
                dzbir =   (suma(fic,405,407,7)-suma(fic,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fic,410,5)==aop(fic,12,5)-aop(fic,404,5)):
                #AOPi
                lzbir =   aop(fic,410,5)
                dzbir =   aop(fic,12,5)-aop(fic,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fic,410,6)==aop(fic,12,6)-aop(fic,404,6)):
                #AOPi
                lzbir =   aop(fic,410,6)
                dzbir =   aop(fic,12,6)-aop(fic,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fic,410,7) == aop(fic,12,7)-aop(fic,404,7)):
                #AOPi
                lzbir =   aop(fic,410,7) 
                dzbir =    aop(fic,12,7)-aop(fic,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fic,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fic,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fic,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1001,5)>0):
                if not(aop(fic,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fic,1002,5)>0):
                if not(aop(fic,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1001,6)>0):
                if not(aop(fic,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fic,1002,6)>0):
                if not(aop(fic,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1003,5)>0):
                if not(aop(fic,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fic,1004,5)>0):
                if not(aop(fic,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1003,6)>0):
                if not(aop(fic,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fic,1004,6)>0):
                if not(aop(fic,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1005,5)>0):
                if not(aop(fic,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fic,1006,5)>0):
                if not(aop(fic,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1005,6)>0):
                if not(aop(fic,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fic,1006,6)>0):
                if not(aop(fic,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1007,5)>0):
                if not(aop(fic,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fic,1008,5)>0):
                if not(aop(fic,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1007,6)>0):
                if not(aop(fic,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fic,1008,6)>0):
                if not(aop(fic,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1009,5)>0):
                if not(aop(fic,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fic,1010,5)>0):
                if not(aop(fic,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1009,6)>0):
                if not(aop(fic,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fic,1010,6)>0):
                if not(aop(fic,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fic,1019,5)==(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fic,1019,5)
                    dzbir = (suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fic,1019,6)==(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fic,1019,6)
                    dzbir = (suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fic,1020,5)==(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fic,1020,5)
                    dzbir = (suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fic,1020,6)==(suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fic,1020,6)
                    dzbir = (suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fic,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fic,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fic,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fic,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1019,5)>0):
                if not(aop(fic,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fic,1020,5)>0):
                if not(aop(fic,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,1019,6)>0):
                if not(aop(fic,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fic,1020,6)>0):
                if not(aop(fic,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fic,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fic,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            #30001
            if not(suma(fic,3001,3039,3)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #30002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fic,3001,3039,4)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fic,3001,3039,4)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30004
            if not(aop(fic,3001,3)==suma_liste(fic,[3002,3003,3004,3005,3006,3007,3008],3)):
                #AOPi
                lzbir = aop(fic,3001,3)
                dzbir = suma_liste(fic,[3002,3003,3004,3005,3006,3007,3008],3)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30005
            if not(aop(fic,3001,4)==suma_liste(fic,[3002,3003,3004,3005,3006,3007,3008],4)):
                #AOPi
                lzbir = aop(fic,3001,4)
                dzbir = suma_liste(fic,[3002,3003,3004,3005,3006,3007,3008],4)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30006
            if not(aop(fic,3009,3)==suma_liste(fic,[3010,3011,3012,3013,3014,3015,3016],3)):
                #AOPi
                lzbir = aop(fic,3009,3)
                dzbir = suma_liste(fic,[3010,3011,3012,3013,3014,3015,3016],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3009 kol. 3 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30007
            if not(aop(fic,3009,4)==suma_liste(fic,[3010,3011,3012,3013,3014,3015,3016],4)):
                #AOPi
                lzbir = aop(fic,3009,4)
                dzbir = suma_liste(fic,[3010,3011,3012,3013,3014,3015,3016],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3009 kol. 4 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30008
            if(aop(fic,3001,3)>aop(fic,3009,3)):
                if not(aop(fic,3017,3)==(aop(fic,3001,3)-aop(fic,3009,3))):
                    #AOPi
                    lzbir = aop(fic,3017,3)
                    dzbir = (aop(fic,3001,3)-aop(fic,3009,3))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP 3017 kol. 3 = AOP-u (3001 - 3009) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3009 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30009
            if(aop(fic,3001,4)>aop(fic,3009,4)):
                if not(aop(fic,3017,4)==(aop(fic,3001,4)-aop(fic,3009,4))):
                    #AOPi
                    lzbir = aop(fic,3017,4)
                    dzbir = (aop(fic,3001,4)-aop(fic,3009,4))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3017 kol. 4 = AOP-u (3001 - 3009) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30010
            if(aop(fic,3001,3)<aop(fic,3009,3)):
                if not(aop(fic,3018,3)==(aop(fic,3009,3)-aop(fic,3001,3))):
                    #AOPi
                    lzbir = aop(fic,3018,3)
                    dzbir = (aop(fic,3009,3)-aop(fic,3001,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3018 kol. 3 = AOP-u (3009 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3009 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30011
            if(aop(fic,3001,4)<aop(fic,3009,4)):
                if not(aop(fic,3018,4)==(aop(fic,3009,4)-aop(fic,3001,4))):
                    #AOPi
                    lzbir = aop(fic,3018,4)
                    dzbir = (aop(fic,3009,4)-aop(fic,3001,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3018 kol. 4 = AOP-u (3009 - 3001) kol. 4,ako je AOP 3001 kol. 4 < AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30012
            if(aop(fic,3001,3)==aop(fic,3009,3)):
                if not(suma(fic,3017,3018,3)==0):
                    #AOPi
                    lzbir = suma(fic,3017,3018,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3009 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30013
            if(aop(fic,3001,4)==aop(fic,3009,4)):
                if not(suma(fic,3017,3018,4)==0):
                    #AOPi
                    lzbir = suma(fic,3017,3018,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3009 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                   
            #30014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3017,3)>0):
                if not(aop(fic,3018,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3017 kol. 3 > 0,onda je AOP 3018 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30015
            if(aop(fic,3018,3)>0):
                if not(aop(fic,3017,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3018 kol. 3 > 0,onda je AOP 3017 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3017,4)>0):
                if not(aop(fic,3018,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3017 kol. 4 > 0,onda je AOP 3018 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30017
            if(aop(fic,3018,4)>0):
                if not(aop(fic,3017,4)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3018 kol. 4 > 0,onda je AOP 3017 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30018
            if not(suma_liste(fic,[3001,3018],3)==suma_liste(fic,[3009,3017],3)):
                #AOPi
                lzbir = suma_liste(fic,[3001,3018],3)
                dzbir = suma_liste(fic,[3009,3017],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3001 + 3018) kol. 3 = AOP-u (3009 + 3017) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30019
            if not(suma_liste(fic,[3001,3018],4)==suma_liste(fic,[3009,3017],4)):
                #AOPi
                lzbir = suma_liste(fic,[3001,3018],4)
                dzbir = suma_liste(fic,[3009,3017],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3001 + 3018) kol. 4 = AOP-u (3009 + 3017) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30020
            if not(aop(fic,3019,3)==suma(fic,3020,3023,3)):
                #AOPi
                lzbir = aop(fic,3019,3)
                dzbir = suma(fic,3020,3023,3)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30021
            if not(aop(fic,3019,4)==suma(fic,3020,3023,4)):
                #AOPi
                lzbir = aop(fic,3019,4)
                dzbir = suma(fic,3020,3023,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30022
            if not(aop(fic,3024,3)==suma(fic,3025,3029,3)):
                #AOPi
                lzbir = aop(fic,3024,3)
                dzbir = suma(fic,3025,3029,3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3024 kol. 3 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30023
            if not(aop(fic,3024,4)==suma(fic,3025,3029,4)):
                #AOPi
                lzbir = aop(fic,3024,4)
                dzbir = suma(fic,3025,3029,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3024 kol. 4 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30024
            if(aop(fic,3019,3)>aop(fic,3024,3)):
                if not(aop(fic,3030,3)==(aop(fic,3019,3)-aop(fic,3024,3))):
                    #AOPi
                    lzbir = aop(fic,3030,3)
                    dzbir = (aop(fic,3019,3)-aop(fic,3024,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP 3030 kol. 3 = AOP-u (3019 - 3024) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3024 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30025
            if(aop(fic,3019,4)>aop(fic,3024,4)):
                if not(aop(fic,3030,4)==(aop(fic,3019,4)-aop(fic,3024,4))):
                    #AOPi
                    lzbir = aop(fic,3030,4)
                    dzbir = (aop(fic,3019,4)-aop(fic,3024,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3030 kol. 4 = AOP-u (3019 - 3024) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30026
            if(aop(fic,3019,3)<aop(fic,3024,3)):
                if not(aop(fic,3031,3)==(aop(fic,3024,3)-aop(fic,3019,3))):
                    #AOPi
                    lzbir = aop(fic,3031,3)
                    dzbir = (aop(fic,3024,3)-aop(fic,3019,3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3031 kol. 3 = AOP-u (3024 - 3019) kol. 3, ako je AOP 3019 kol. 3 < AOP-a 3024 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30027
            if(aop(fic,3019,4)<aop(fic,3024,4)):
                if not(aop(fic,3031,4)==(aop(fic,3024,4)-aop(fic,3019,4))):
                    #AOPi
                    lzbir = aop(fic,3031,4)
                    dzbir = (aop(fic,3024,4)-aop(fic,3019,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3031 kol. 4 = AOP-u (3024 - 3019) kol. 4, ako je AOP 3019 kol. 4 < AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30028
            if(aop(fic,3019,3)==aop(fic,3024,3)):
                if not(suma(fic,3030,3031,3)==0):
                    #AOPi
                    lzbir = suma(fic,3030,3031,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3024 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30029
            if(aop(fic,3019,4)==aop(fic,3024,4)):
                if not(suma(fic,3030,3031,4)==0):
                    #AOPi
                    lzbir = suma(fic,3030,3031,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3024 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3030,3)>0):
                if not(aop(fic,3031,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3030 kol. 3 > 0,onda je AOP 3031 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30031
            if(aop(fic,3031,3)>0):
                if not(aop(fic,3030,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3031 kol. 3 > 0,onda je AOP 3030 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3030,4)>0):
                if not(aop(fic,3031,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   Ako je AOP 3030 kol. 4 > 0,onda je AOP 3031 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30033
            if(aop(fic,3031,4)>0):
                if not(aop(fic,3030,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   Ako je AOP 3031 kol. 4 > 0,onda je AOP 3030 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30034
            if not(suma_liste(fic,[3019,3031],3)==suma_liste(fic,[3024,3030],3)):
                #AOPi
                lzbir = suma_liste(fic,[3019,3031],3)
                dzbir = suma_liste(fic,[3024,3030],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3019 + 3031) kol. 3 = AOP-u (3024 + 3030) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30035
            if not(suma_liste(fic,[3019,3031],4)==suma_liste(fic,[3024,3030],4)):
                #AOPi
                lzbir = suma_liste(fic,[3019,3031],4)
                dzbir = suma_liste(fic,[3024,3030],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3019 + 3031) kol. 4 = AOP-u (3024 + 3030) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30036
            if not(aop(fic,3032,3)==suma_liste(fic,[3017,3030],3)):
                #AOPi
                lzbir = aop(fic,3032,3)
                dzbir = suma_liste(fic,[3017,3030],3)
                razlika = lzbir - dzbir     
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3032 kol. 3 = AOP-u (3017 + 3030) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30037
            if not(aop(fic,3032,4)==suma_liste(fic,[3017,3030],4)):
                #AOPi
                lzbir = aop(fic,3032,4)
                dzbir = suma_liste(fic,[3017,3030],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3032 kol. 4 = AOP-u (3017 + 3030) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30038
            if not(aop(fic,3033,3)==suma_liste(fic,[3018,3031],3)):
                #AOPi
                lzbir = aop(fic,3033,3)
                dzbir = suma_liste(fic,[3018,3031],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="   AOP 3033 kol. 3 = AOP-u (3018 + 3031) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30039
            if not(aop(fic,3033,4)==suma_liste(fic,[3018,3031],4)):
                #AOPi
                lzbir = aop(fic,3033,4)
                dzbir = suma_liste(fic,[3018,3031],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="   AOP 3033 kol. 4 = AOP-u (3018 + 3031) kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30040
            if(aop(fic,3032,3)>aop(fic,3033,3)):
                if not(aop(fic,3034,3)==(aop(fic,3032,3)-aop(fic,3033,3))):
                    #AOPi
                    lzbir = aop(fic,3034,3)
                    dzbir = (aop(fic,3032,3)-aop(fic,3033,3))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3034 kol. 3 = AOP-u (3032 - 3033) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30041
            if(aop(fic,3032,4)>aop(fic,3033,4)):
                if not(aop(fic,3034,4)==(aop(fic,3032,4)-aop(fic,3033,4))):
                    #AOPi
                    lzbir = aop(fic,3034,4)
                    dzbir = (aop(fic,3032,4)-aop(fic,3033,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP 3034 kol. 4 = AOP-u (3032 - 3033) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3033 kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30042
            if(aop(fic,3032,3)<aop(fic,3033,3)):
                if not(aop(fic,3035,3)==(aop(fic,3033,3)-aop(fic,3032,3))):
                    #AOPi
                    lzbir = aop(fic,3035,3)
                    dzbir = (aop(fic,3033,3)-aop(fic,3032,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3035 kol. 3 = AOP-u (3033 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30043    
            if(aop(fic,3032,4)<aop(fic,3033,4)):
                if not(aop(fic,3035,4)==(aop(fic,3033,4)-aop(fic,3032,4))):
                    #AOPi
                    lzbir = aop(fic,3035,4)
                    dzbir = (aop(fic,3033,4)-aop(fic,3032,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3035 kol. 4 = AOP-u (3033 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3033 kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30044    
            if(aop(fic,3032,3)==aop(fic,3033,3)):
                if not(suma(fic,3034,3035,3)==0):
                    #AOPi
                    lzbir = suma(fic,3034,3035,3)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (3034 + 3035) kol. 3 = 0, ako je AOP 3032 kol. 3 = AOP-u 3033 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30045    
            if(aop(fic,3032,4)==aop(fic,3033,4)):
                if not(suma(fic,3034,3035,4)==0):
                    #AOPi
                    lzbir = suma(fic,3034,3035,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP (3034 + 3035) kol. 4 = 0, ako je AOP 3032 kol. 4 = AOP-u 3033 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30046 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3034,3)>0):
                if not(aop(fic,3035,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3034 kol. 3 > 0,onda je AOP 3035 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30047    
            if(aop(fic,3035,3)>0):
                if not(aop(fic,3034,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3035 kol. 3 > 0,onda je AOP 3034 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30048 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,3034,4)>0):
                if not(aop(fic,3035,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30049
            if(aop(fic,3035,4)>0):
                if not(aop(fic,3034,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30050
            if not(suma_liste(fic,[3032,3035],3)==suma_liste(fic,[3033,3034],3)):
                #AOPi
                lzbir = suma_liste(fic,[3032,3035],3)
                dzbir = suma_liste(fic,[3033,3034],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3032 + 3035) kol. 3 = AOP-u (3033 + 3034) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30051
            if not(suma_liste(fic,[3032,3035],4)==suma_liste(fic,[3033,3034],4)):
                #AOPi
                lzbir = suma_liste(fic,[3032,3035],4)
                dzbir = suma_liste(fic,[3033,3034],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (3032 + 3035) kol. 4 = AOP-u (3033 + 3034) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30052
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(aop(fic,3036,3)==0):
                    hasWarning=True 
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3036 kol. 3 = 0; Novoosnovana pravna lica po pravilu ne smeju imati prikazan podatak za prethodnu godinu "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                
            #30053
            if(suma_liste(fic,[3034,3036,3037],3)>suma_liste(fic,[3035,3038],3)):
                if not(aop(fic,3039,3)==(suma_liste(fic,[3034,3036,3037],3)-suma_liste(fic,[3035,3038],3))):
                    #AOPi
                    lzbir = aop(fic,3039,3)
                    dzbir = (suma_liste(fic,[3034,3036,3037],3)-suma_liste(fic,[3035,3038],3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP 3039 kol. 3 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 3, ako je AOP (3034 + 3036 + 3037) kol. 3 > AOP-a (3035 + 3038) kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30054
            if(suma_liste(fic,[3034,3036,3037],4)>suma_liste(fic,[3035,3038],4)):
                if not(aop(fic,3039,4)==(suma_liste(fic,[3034,3036,3037],4)-suma_liste(fic,[3035,3038],4))):
                    #AOPi
                    lzbir = aop(fic,3039,4)
                    dzbir = (suma_liste(fic,[3034,3036,3037],4)-suma_liste(fic,[3035,3038],4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="   AOP 3039 kol. 4 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 4, ako je AOP (3034 + 3036 + 3037) kol. 4 > AOP-a (3035 + 3038) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30055
            if(suma_liste(fic,[3034,3036,3037],3)<=suma_liste(fic,[3035,3038],3)):
                if not(aop(fic,3039,3)==0):   
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3039 kol. 3 = 0, ako je AOP (3034 + 3036 + 3037) kol. 3 ≤ AOP-a (3035 + 3038) kol. 3 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30056
            if(suma_liste(fic,[3034,3036,3037],4)<=suma_liste(fic,[3035,3038],4)):
                if not(aop(fic,3039,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 3039 kol. 4 = 0, ako je AOP (3034 + 3036 + 3037) kol. 4 ≤ AOP-a (3035 + 3038) kol. 4 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30057
            if not(aop(fic,3039,4)==aop(fic,3036,3)):
                #AOPi
                lzbir = aop(fic,3039,4)
                dzbir = aop(fic,3036,3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 3036 kol. 3   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30058
            if not(aop(fic,3039,3)==aop(fic,1,5)):
                #AOPi
                lzbir = aop(fic,3039,3)
                dzbir = aop(fic,1,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3039 kol. 3 = AOP-u 0001 kol. 5 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                
            #30059
            if not(aop(fic,3039,4)==aop(fic,1,6)):
                #AOPi
                lzbir = aop(fic,3039,4)
                dzbir = aop(fic,1,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 0001 kol. 6 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40001    
            if not(suma(fic,4001,4015,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 5 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #40002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):    
                if not(suma(fic,4001,4015,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 = 0; Izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #40003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):    
                if not(suma(fic,4001,4015,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
            #40004
            if(suma_liste(fic,[4002,4004,4005,4006,4007],5)>suma_liste(fic,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fic,4013,5)==(suma_liste(fic,[4002,4004,4005,4006,4007],5)-suma_liste(fic,[4003,4008,4009,4010,4011,4012],5))):
                    #AOPi
                    lzbir = aop(fic,4013,5)
                    dzbir = (suma_liste(fic,[4002,4004,4005,4006,4007],5)-suma_liste(fic,[4003,4008,4009,4010,4011,4012],5))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 4013 kol. 5 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #40005
            if(suma_liste(fic,[4002,4004,4005,4006,4007],6)>suma_liste(fic,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fic,4013,6)==(suma_liste(fic,[4002,4004,4005,4006,4007],6)-suma_liste(fic,[4003,4008,4009,4010,4011,4012],6))):
                    #AOPi
                    lzbir = aop(fic,4013,6)
                    dzbir = (suma_liste(fic,[4002,4004,4005,4006,4007],6)-suma_liste(fic,[4003,4008,4009,4010,4011,4012],6))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 4013 kol. 6 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40006
            if(suma_liste(fic,[4002,4004,4005,4006,4007],5)<suma_liste(fic,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fic,4014,5)==(suma_liste(fic,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fic,[4002,4004,4005,4006,4007],5))):
                    #AOPi
                    lzbir = aop(fic,4014,5)
                    dzbir = (suma_liste(fic,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fic,[4002,4004,4005,4006,4007],5))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 4014 kol. 5 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40007
            if(suma_liste(fic,[4002,4004,4005,4006,4007],6)<suma_liste(fic,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fic,4014,6)==(suma_liste(fic,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fic,[4002,4004,4005,4006,4007],6))):
                    #AOPi
                    lzbir = aop(fic,4014,6)
                    dzbir = (suma_liste(fic,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fic,[4002,4004,4005,4006,4007],6))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP 4014 kol. 6 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40008
            if(suma_liste(fic,[4002,4004,4005,4006,4007],5) == suma_liste(fic,[4003,4008,4009,4010,4011,4012],5)):
                if not(suma(fic,4013,4014,5)== 0):
                    #AOPi
                    lzbir = suma(fic,4013,4014,5)
                    dzbir =  0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (4013 + 4014) kol. 5 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #40009
            if(suma_liste(fic,[4002,4004,4005,4006,4007],6) == suma_liste(fic,[4003,4008,4009,4010,4011,4012],6)):
                if not(suma(fic,4013,4014,6)== 0):
                    #AOPi
                    lzbir = suma(fic,4013,4014,6)
                    dzbir =  0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    AOP (4013 + 4014) kol. 6 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,4013,5)>0):
                if not(aop(fic,4014,5)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 4013 kol. 5 > 0,onda je AOP 4014 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40011    
            if(aop(fic,4014,5)>0):
                if not(aop(fic,4013,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 4014 kol. 5 > 0,onda je AOP 4013 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fic,4013,6)>0):
                if not(aop(fic,4014,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 4013 kol. 6 > 0,onda je AOP 4014 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40013   
            if(aop(fic,4014,6)>0):
                if not(aop(fic,4013,6)==0):  
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 3'
                    poruka  ="    Ako je AOP 4014 kol. 6 > 0,onda je AOP 4013 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40014
            if not(suma_liste(fic,[4002,4004,4005,4006,4007,4014],5)==suma_liste(fic,[4003,4008,4009,4010,4011,4012,4013],5)):
                #AOPi
                lzbir = suma_liste(fic,[4002,4004,4005,4006,4007,4014],5)
                dzbir = suma_liste(fic,[4003,4008,4009,4010,4011,4012,4013],5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40015
            if not(suma_liste(fic,[4002,4004,4005,4006,4007,4014],6)==suma_liste(fic,[4003,4008,4009,4010,4011,4012,4013],6)):
                #AOPi
                lzbir = suma_liste(fic,[4002,4004,4005,4006,4007,4014],6)
                dzbir = suma_liste(fic,[4003,4008,4009,4010,4011,4012,4013],6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže;  Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40016
            if not(aop(fic,4015,5)==(suma_liste(fic,[4001,4013],5)-aop(fic,4014,5))):
                #AOPi
                lzbir = aop(fic,4015,5)
                dzbir = (suma_liste(fic,[4001,4013],5)-aop(fic,4014,5))
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4015 kol. 5 = AOP-u (4001 + 4013 - 4014) kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40017
            if not(aop(fic,4015,6)==(suma_liste(fic,[4001,4013],6)-aop(fic,4014,6))):
                #AOPi
                lzbir = aop(fic,4015,6)
                dzbir = (suma_liste(fic,[4001,4013],6)-aop(fic,4014,6))
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4015 kol. 6 = AOP-u (4001 + 4013 - 4014) kol. 6     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40018
            if not(aop(fic,4015,6)==aop(fic,4001,5)):
                #AOPi
                lzbir = aop(fic,4015,6)
                dzbir = aop(fic,4001,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 4001 kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            
            #40019
            if not(aop(fic,4001,6)==aop(fic,410,7)):
                #AOPi
                lzbir = aop(fic,4001,6)
                dzbir = aop(fic,410,7)
                razlika = lzbir - dzbir
                hasWarning=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4001 kol. 6 = AOP-u 0410 kol. 7 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40020
            if not(aop(fic,4002,5)==aop(fic,406,5)):
                #AOPi
                lzbir = aop(fic,4002,5)
                dzbir = aop(fic,406,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4002 kol. 5 = AOP-u 0406 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40021
            if not(aop(fic,4002,6)==aop(fic,406,6)):
                #AOPi
                lzbir = aop(fic,4002,6)
                dzbir = aop(fic,406,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4002 kol. 6 = AOP-u 0406 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40022
            if not(aop(fic,4003,5)==aop(fic,408,5)):
                #AOPi
                lzbir = aop(fic,4003,5)
                dzbir = aop(fic,408,5)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4003 kol. 5 = AOP-u 0408 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40023
            if not(aop(fic,4003,6)==aop(fic,408,6)):
                #AOPi
                lzbir = aop(fic,4003,6)
                dzbir = aop(fic,408,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4003 kol. 6 = AOP-u 0408 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40024
            if not(aop(fic,4015,5)==aop(fic,410,5)):
                #AOPi
                lzbir = aop(fic,4015,5)
                dzbir = aop(fic,410,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4015 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40025
            if not(aop(fic,4015,6)==aop(fic,410,6)):
                #AOPi
                lzbir = aop(fic,4015,6)
                dzbir = aop(fic,410,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 3'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND3----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND3----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 4 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fid,1,12,5) + suma(fid,401,410,5) + suma(fid,1,12,6) + suma(fid,401,410,6) + suma(fid,1,12,7) + suma(fid,401,410,7) + suma(fid,1001,1020,5) + suma(fid,1001,1020,6) + suma(fid,3001,3039,3) + suma(fid,3001,3039,4) + suma(fid,4001,4015,5) + suma(fid,4001,4015,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 4'
            poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 + (0001 do 0410) kol. 6 + (0001 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha + (3001 do 3039) kol. 3 + (3001 do 3039) kol. 4 izveštaja o tokovima gotovine + (4001 do 4015) kol. 5 + (4001 do 4015) kol. 6 izveštaja o promenama na neto imovini > 0; Ukoliko podaci za FOND 1 nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga."
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fid,1,12,5) + suma(fid,401,410,5) + suma(fid,1,12,6) + suma(fid,401,410,6) + suma(fid,1,12,7) + suma(fid,401,410,7) + suma(fid,1001,1020,5) + suma(fid,1001,1020,6) + suma(fid,3001,3039,3) + suma(fid,3001,3039,4) + suma(fid,4001,4015,5) + suma(fid,4001,4015,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 4'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND4----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND4----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 4'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00000-3 
            # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
            fidNapomene = Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme;

            if not(proveriNapomene(fidNapomene, 1, 12, 4) or proveriNapomene(fidNapomene, 401, 410, 4) or proveriNapomene(fidNapomene, 1001, 1020, 4) or proveriNapomene(fidNapomene, 4001, 4015, 4)):
                hasError = True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="Na AOP-u (0001 do 0012) bilansa stanja-izveštaja o neto imovini + (0401 do 0410) bilansa stanja-izveštaja o neto imovini + (1001 do 1020) bilansa uspeha + (4001 do 4015) izveštaja o promenama na neto imovini u koloni 4 (Napomena) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00001
            if not((suma(fid,1,12,5)+suma(fid,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fid,1,12,6)+suma(fid,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fid,1,12,7)+suma(fid,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fid,1,12,6)+suma(fid,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fid,1,12,7)+suma(fid,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fid,12,5)==suma(fid,1,11,5)):
                #AOPi
                lzbir =   aop(fid,12,5)
                dzbir =   suma(fid,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fid,12,6)==suma(fid,1,11,6)):
                #AOPi
                lzbir =   aop(fid,12,6)
                dzbir =   suma(fid,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fid,12,7)==suma(fid,1,11,7)):
                #AOPi
                lzbir =   aop(fid,12,7)
                dzbir =   suma(fid,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fid,404,5)== suma(fid,401,403,5)):
                #AOPi
                lzbir =   aop(fid,404,5)
                dzbir =   suma(fid,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fid,404,6)== suma(fid,401,403,6)):
                #AOPi
                lzbir =   aop(fid,404,6)
                dzbir =   suma(fid,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fid,404,7)==suma(fid,401,403,7)):
                #AOPi
                lzbir =   aop(fid,404,7)
                dzbir =   suma(fid,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fid,410,5)==(suma(fid,405,407,5)-suma(fid,408,409,5))):
                #AOPi
                lzbir =   aop(fid,410,5)
                dzbir =   (suma(fid,405,407,5)-suma(fid,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fid,410,6)==(suma(fid,405,407,6)-suma(fid,408,409,6))):
                #AOPi
                lzbir =   aop(fid,410,6)
                dzbir =   (suma(fid,405,407,6)-suma(fid,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fid,410,7)==(suma(fid,405,407,7)-suma(fid,408,409,7))):
                #AOPi
                lzbir =   aop(fid,410,7)
                dzbir =   (suma(fid,405,407,7)-suma(fid,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fid,410,5)==aop(fid,12,5)-aop(fid,404,5)):
                #AOPi
                lzbir =   aop(fid,410,5)
                dzbir =   aop(fid,12,5)-aop(fid,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fid,410,6)==aop(fid,12,6)-aop(fid,404,6)):
                #AOPi
                lzbir =   aop(fid,410,6)
                dzbir =   aop(fid,12,6)-aop(fid,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fid,410,7) == aop(fid,12,7)-aop(fid,404,7)):
                #AOPi
                lzbir =   aop(fid,410,7) 
                dzbir =    aop(fid,12,7)-aop(fid,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fid,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fid,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fid,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1001,5)>0):
                if not(aop(fid,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fid,1002,5)>0):
                if not(aop(fid,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1001,6)>0):
                if not(aop(fid,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fid,1002,6)>0):
                if not(aop(fid,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1003,5)>0):
                if not(aop(fid,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fid,1004,5)>0):
                if not(aop(fid,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1003,6)>0):
                if not(aop(fid,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fid,1004,6)>0):
                if not(aop(fid,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1005,5)>0):
                if not(aop(fid,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fid,1006,5)>0):
                if not(aop(fid,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1005,6)>0):
                if not(aop(fid,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fid,1006,6)>0):
                if not(aop(fid,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1007,5)>0):
                if not(aop(fid,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fid,1008,5)>0):
                if not(aop(fid,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1007,6)>0):
                if not(aop(fid,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fid,1008,6)>0):
                if not(aop(fid,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1009,5)>0):
                if not(aop(fid,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fid,1010,5)>0):
                if not(aop(fid,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1009,6)>0):
                if not(aop(fid,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fid,1010,6)>0):
                if not(aop(fid,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fid,1019,5)==(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fid,1019,5)
                    dzbir = (suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fid,1019,6)==(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fid,1019,6)
                    dzbir = (suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fid,1020,5)==(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fid,1020,5)
                    dzbir = (suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fid,1020,6)==(suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fid,1020,6)
                    dzbir = (suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fid,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fid,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fid,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fid,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1019,5)>0):
                if not(aop(fid,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fid,1020,5)>0):
                if not(aop(fid,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,1019,6)>0):
                if not(aop(fid,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fid,1020,6)>0):
                if not(aop(fid,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fid,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fid,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            #30001
            if not(suma(fid,3001,3039,3)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #30002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fid,3001,3039,4)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fid,3001,3039,4)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30004
            if not(aop(fid,3001,3)==suma_liste(fid,[3002,3003,3004,3005,3006,3007,3008],3)):
                #AOPi
                lzbir = aop(fid,3001,3)
                dzbir = suma_liste(fid,[3002,3003,3004,3005,3006,3007,3008],3)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30005
            if not(aop(fid,3001,4)==suma_liste(fid,[3002,3003,3004,3005,3006,3007,3008],4)):
                #AOPi
                lzbir = aop(fid,3001,4)
                dzbir = suma_liste(fid,[3002,3003,3004,3005,3006,3007,3008],4)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30006
            if not(aop(fid,3009,3)==suma_liste(fid,[3010,3011,3012,3013,3014,3015,3016],3)):
                #AOPi
                lzbir = aop(fid,3009,3)
                dzbir = suma_liste(fid,[3010,3011,3012,3013,3014,3015,3016],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3009 kol. 3 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30007
            if not(aop(fid,3009,4)==suma_liste(fid,[3010,3011,3012,3013,3014,3015,3016],4)):
                #AOPi
                lzbir = aop(fid,3009,4)
                dzbir = suma_liste(fid,[3010,3011,3012,3013,3014,3015,3016],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3009 kol. 4 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30008
            if(aop(fid,3001,3)>aop(fid,3009,3)):
                if not(aop(fid,3017,3)==(aop(fid,3001,3)-aop(fid,3009,3))):
                    #AOPi
                    lzbir = aop(fid,3017,3)
                    dzbir = (aop(fid,3001,3)-aop(fid,3009,3))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP 3017 kol. 3 = AOP-u (3001 - 3009) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3009 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30009
            if(aop(fid,3001,4)>aop(fid,3009,4)):
                if not(aop(fid,3017,4)==(aop(fid,3001,4)-aop(fid,3009,4))):
                    #AOPi
                    lzbir = aop(fid,3017,4)
                    dzbir = (aop(fid,3001,4)-aop(fid,3009,4))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3017 kol. 4 = AOP-u (3001 - 3009) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30010
            if(aop(fid,3001,3)<aop(fid,3009,3)):
                if not(aop(fid,3018,3)==(aop(fid,3009,3)-aop(fid,3001,3))):
                    #AOPi
                    lzbir = aop(fid,3018,3)
                    dzbir = (aop(fid,3009,3)-aop(fid,3001,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3018 kol. 3 = AOP-u (3009 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3009 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30011
            if(aop(fid,3001,4)<aop(fid,3009,4)):
                if not(aop(fid,3018,4)==(aop(fid,3009,4)-aop(fid,3001,4))):
                    #AOPi
                    lzbir = aop(fid,3018,4)
                    dzbir = (aop(fid,3009,4)-aop(fid,3001,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3018 kol. 4 = AOP-u (3009 - 3001) kol. 4,ako je AOP 3001 kol. 4 < AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30012
            if(aop(fid,3001,3)==aop(fid,3009,3)):
                if not(suma(fid,3017,3018,3)==0):
                    #AOPi
                    lzbir = suma(fid,3017,3018,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3009 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30013
            if(aop(fid,3001,4)==aop(fid,3009,4)):
                if not(suma(fid,3017,3018,4)==0):
                    #AOPi
                    lzbir = suma(fid,3017,3018,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3009 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                   
            #30014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3017,3)>0):
                if not(aop(fid,3018,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3017 kol. 3 > 0,onda je AOP 3018 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30015
            if(aop(fid,3018,3)>0):
                if not(aop(fid,3017,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3018 kol. 3 > 0,onda je AOP 3017 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3017,4)>0):
                if not(aop(fid,3018,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3017 kol. 4 > 0,onda je AOP 3018 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30017
            if(aop(fid,3018,4)>0):
                if not(aop(fid,3017,4)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3018 kol. 4 > 0,onda je AOP 3017 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30018
            if not(suma_liste(fid,[3001,3018],3)==suma_liste(fid,[3009,3017],3)):
                #AOPi
                lzbir = suma_liste(fid,[3001,3018],3)
                dzbir = suma_liste(fid,[3009,3017],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3001 + 3018) kol. 3 = AOP-u (3009 + 3017) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30019
            if not(suma_liste(fid,[3001,3018],4)==suma_liste(fid,[3009,3017],4)):
                #AOPi
                lzbir = suma_liste(fid,[3001,3018],4)
                dzbir = suma_liste(fid,[3009,3017],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3001 + 3018) kol. 4 = AOP-u (3009 + 3017) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30020
            if not(aop(fid,3019,3)==suma(fid,3020,3023,3)):
                #AOPi
                lzbir = aop(fid,3019,3)
                dzbir = suma(fid,3020,3023,3)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30021
            if not(aop(fid,3019,4)==suma(fid,3020,3023,4)):
                #AOPi
                lzbir = aop(fid,3019,4)
                dzbir = suma(fid,3020,3023,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30022
            if not(aop(fid,3024,3)==suma(fid,3025,3029,3)):
                #AOPi
                lzbir = aop(fid,3024,3)
                dzbir = suma(fid,3025,3029,3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3024 kol. 3 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30023
            if not(aop(fid,3024,4)==suma(fid,3025,3029,4)):
                #AOPi
                lzbir = aop(fid,3024,4)
                dzbir = suma(fid,3025,3029,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3024 kol. 4 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30024
            if(aop(fid,3019,3)>aop(fid,3024,3)):
                if not(aop(fid,3030,3)==(aop(fid,3019,3)-aop(fid,3024,3))):
                    #AOPi
                    lzbir = aop(fid,3030,3)
                    dzbir = (aop(fid,3019,3)-aop(fid,3024,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP 3030 kol. 3 = AOP-u (3019 - 3024) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3024 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30025
            if(aop(fid,3019,4)>aop(fid,3024,4)):
                if not(aop(fid,3030,4)==(aop(fid,3019,4)-aop(fid,3024,4))):
                    #AOPi
                    lzbir = aop(fid,3030,4)
                    dzbir = (aop(fid,3019,4)-aop(fid,3024,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3030 kol. 4 = AOP-u (3019 - 3024) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30026
            if(aop(fid,3019,3)<aop(fid,3024,3)):
                if not(aop(fid,3031,3)==(aop(fid,3024,3)-aop(fid,3019,3))):
                    #AOPi
                    lzbir = aop(fid,3031,3)
                    dzbir = (aop(fid,3024,3)-aop(fid,3019,3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3031 kol. 3 = AOP-u (3024 - 3019) kol. 3, ako je AOP 3019 kol. 3 < AOP-a 3024 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30027
            if(aop(fid,3019,4)<aop(fid,3024,4)):
                if not(aop(fid,3031,4)==(aop(fid,3024,4)-aop(fid,3019,4))):
                    #AOPi
                    lzbir = aop(fid,3031,4)
                    dzbir = (aop(fid,3024,4)-aop(fid,3019,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3031 kol. 4 = AOP-u (3024 - 3019) kol. 4, ako je AOP 3019 kol. 4 < AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30028
            if(aop(fid,3019,3)==aop(fid,3024,3)):
                if not(suma(fid,3030,3031,3)==0):
                    #AOPi
                    lzbir = suma(fid,3030,3031,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3024 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30029
            if(aop(fid,3019,4)==aop(fid,3024,4)):
                if not(suma(fid,3030,3031,4)==0):
                    #AOPi
                    lzbir = suma(fid,3030,3031,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3024 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3030,3)>0):
                if not(aop(fid,3031,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3030 kol. 3 > 0,onda je AOP 3031 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30031
            if(aop(fid,3031,3)>0):
                if not(aop(fid,3030,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3031 kol. 3 > 0,onda je AOP 3030 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3030,4)>0):
                if not(aop(fid,3031,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   Ako je AOP 3030 kol. 4 > 0,onda je AOP 3031 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30033
            if(aop(fid,3031,4)>0):
                if not(aop(fid,3030,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   Ako je AOP 3031 kol. 4 > 0,onda je AOP 3030 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30034
            if not(suma_liste(fid,[3019,3031],3)==suma_liste(fid,[3024,3030],3)):
                #AOPi
                lzbir = suma_liste(fid,[3019,3031],3)
                dzbir = suma_liste(fid,[3024,3030],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3019 + 3031) kol. 3 = AOP-u (3024 + 3030) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30035
            if not(suma_liste(fid,[3019,3031],4)==suma_liste(fid,[3024,3030],4)):
                #AOPi
                lzbir = suma_liste(fid,[3019,3031],4)
                dzbir = suma_liste(fid,[3024,3030],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3019 + 3031) kol. 4 = AOP-u (3024 + 3030) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30036
            if not(aop(fid,3032,3)==suma_liste(fid,[3017,3030],3)):
                #AOPi
                lzbir = aop(fid,3032,3)
                dzbir = suma_liste(fid,[3017,3030],3)
                razlika = lzbir - dzbir     
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3032 kol. 3 = AOP-u (3017 + 3030) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30037
            if not(aop(fid,3032,4)==suma_liste(fid,[3017,3030],4)):
                #AOPi
                lzbir = aop(fid,3032,4)
                dzbir = suma_liste(fid,[3017,3030],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3032 kol. 4 = AOP-u (3017 + 3030) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30038
            if not(aop(fid,3033,3)==suma_liste(fid,[3018,3031],3)):
                #AOPi
                lzbir = aop(fid,3033,3)
                dzbir = suma_liste(fid,[3018,3031],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="   AOP 3033 kol. 3 = AOP-u (3018 + 3031) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30039
            if not(aop(fid,3033,4)==suma_liste(fid,[3018,3031],4)):
                #AOPi
                lzbir = aop(fid,3033,4)
                dzbir = suma_liste(fid,[3018,3031],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="   AOP 3033 kol. 4 = AOP-u (3018 + 3031) kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30040
            if(aop(fid,3032,3)>aop(fid,3033,3)):
                if not(aop(fid,3034,3)==(aop(fid,3032,3)-aop(fid,3033,3))):
                    #AOPi
                    lzbir = aop(fid,3034,3)
                    dzbir = (aop(fid,3032,3)-aop(fid,3033,3))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3034 kol. 3 = AOP-u (3032 - 3033) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30041
            if(aop(fid,3032,4)>aop(fid,3033,4)):
                if not(aop(fid,3034,4)==(aop(fid,3032,4)-aop(fid,3033,4))):
                    #AOPi
                    lzbir = aop(fid,3034,4)
                    dzbir = (aop(fid,3032,4)-aop(fid,3033,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP 3034 kol. 4 = AOP-u (3032 - 3033) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3033 kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30042
            if(aop(fid,3032,3)<aop(fid,3033,3)):
                if not(aop(fid,3035,3)==(aop(fid,3033,3)-aop(fid,3032,3))):
                    #AOPi
                    lzbir = aop(fid,3035,3)
                    dzbir = (aop(fid,3033,3)-aop(fid,3032,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3035 kol. 3 = AOP-u (3033 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30043    
            if(aop(fid,3032,4)<aop(fid,3033,4)):
                if not(aop(fid,3035,4)==(aop(fid,3033,4)-aop(fid,3032,4))):
                    #AOPi
                    lzbir = aop(fid,3035,4)
                    dzbir = (aop(fid,3033,4)-aop(fid,3032,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3035 kol. 4 = AOP-u (3033 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3033 kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30044    
            if(aop(fid,3032,3)==aop(fid,3033,3)):
                if not(suma(fid,3034,3035,3)==0):
                    #AOPi
                    lzbir = suma(fid,3034,3035,3)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (3034 + 3035) kol. 3 = 0, ako je AOP 3032 kol. 3 = AOP-u 3033 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30045    
            if(aop(fid,3032,4)==aop(fid,3033,4)):
                if not(suma(fid,3034,3035,4)==0):
                    #AOPi
                    lzbir = suma(fid,3034,3035,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP (3034 + 3035) kol. 4 = 0, ako je AOP 3032 kol. 4 = AOP-u 3033 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30046 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3034,3)>0):
                if not(aop(fid,3035,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3034 kol. 3 > 0,onda je AOP 3035 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30047    
            if(aop(fid,3035,3)>0):
                if not(aop(fid,3034,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3035 kol. 3 > 0,onda je AOP 3034 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30048 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,3034,4)>0):
                if not(aop(fid,3035,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30049
            if(aop(fid,3035,4)>0):
                if not(aop(fid,3034,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30050
            if not(suma_liste(fid,[3032,3035],3)==suma_liste(fid,[3033,3034],3)):
                #AOPi
                lzbir = suma_liste(fid,[3032,3035],3)
                dzbir = suma_liste(fid,[3033,3034],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3032 + 3035) kol. 3 = AOP-u (3033 + 3034) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30051
            if not(suma_liste(fid,[3032,3035],4)==suma_liste(fid,[3033,3034],4)):
                #AOPi
                lzbir = suma_liste(fid,[3032,3035],4)
                dzbir = suma_liste(fid,[3033,3034],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (3032 + 3035) kol. 4 = AOP-u (3033 + 3034) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30052
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(aop(fid,3036,3)==0):
                    hasWarning=True 
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3036 kol. 3 = 0; Novoosnovana pravna lica po pravilu ne smeju imati prikazan podatak za prethodnu godinu "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                
            #30053
            if(suma_liste(fid,[3034,3036,3037],3)>suma_liste(fid,[3035,3038],3)):
                if not(aop(fid,3039,3)==(suma_liste(fid,[3034,3036,3037],3)-suma_liste(fid,[3035,3038],3))):
                    #AOPi
                    lzbir = aop(fid,3039,3)
                    dzbir = (suma_liste(fid,[3034,3036,3037],3)-suma_liste(fid,[3035,3038],3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP 3039 kol. 3 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 3, ako je AOP (3034 + 3036 + 3037) kol. 3 > AOP-a (3035 + 3038) kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30054
            if(suma_liste(fid,[3034,3036,3037],4)>suma_liste(fid,[3035,3038],4)):
                if not(aop(fid,3039,4)==(suma_liste(fid,[3034,3036,3037],4)-suma_liste(fid,[3035,3038],4))):
                    #AOPi
                    lzbir = aop(fid,3039,4)
                    dzbir = (suma_liste(fid,[3034,3036,3037],4)-suma_liste(fid,[3035,3038],4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="   AOP 3039 kol. 4 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 4, ako je AOP (3034 + 3036 + 3037) kol. 4 > AOP-a (3035 + 3038) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30055
            if(suma_liste(fid,[3034,3036,3037],3)<=suma_liste(fid,[3035,3038],3)):
                if not(aop(fid,3039,3)==0):   
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3039 kol. 3 = 0, ako je AOP (3034 + 3036 + 3037) kol. 3 ≤ AOP-a (3035 + 3038) kol. 3 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30056
            if(suma_liste(fid,[3034,3036,3037],4)<=suma_liste(fid,[3035,3038],4)):
                if not(aop(fid,3039,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 3039 kol. 4 = 0, ako je AOP (3034 + 3036 + 3037) kol. 4 ≤ AOP-a (3035 + 3038) kol. 4 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30057
            if not(aop(fid,3039,4)==aop(fid,3036,3)):
                #AOPi
                lzbir = aop(fid,3039,4)
                dzbir = aop(fid,3036,3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 3036 kol. 3   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30058
            if not(aop(fid,3039,3)==aop(fid,1,5)):
                #AOPi
                lzbir = aop(fid,3039,3)
                dzbir = aop(fid,1,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3039 kol. 3 = AOP-u 0001 kol. 5 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                
            #30059
            if not(aop(fid,3039,4)==aop(fid,1,6)):
                #AOPi
                lzbir = aop(fid,3039,4)
                dzbir = aop(fid,1,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 0001 kol. 6 bilansa stanja;Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40001    
            if not(suma(fid,4001,4015,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 5 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #40002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):    
                if not(suma(fid,4001,4015,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 = 0; Izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #40003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):    
                if not(suma(fid,4001,4015,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
            #40004
            if(suma_liste(fid,[4002,4004,4005,4006,4007],5)>suma_liste(fid,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fid,4013,5)==(suma_liste(fid,[4002,4004,4005,4006,4007],5)-suma_liste(fid,[4003,4008,4009,4010,4011,4012],5))):
                    #AOPi
                    lzbir = aop(fid,4013,5)
                    dzbir = (suma_liste(fid,[4002,4004,4005,4006,4007],5)-suma_liste(fid,[4003,4008,4009,4010,4011,4012],5))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 4013 kol. 5 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #40005
            if(suma_liste(fid,[4002,4004,4005,4006,4007],6)>suma_liste(fid,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fid,4013,6)==(suma_liste(fid,[4002,4004,4005,4006,4007],6)-suma_liste(fid,[4003,4008,4009,4010,4011,4012],6))):
                    #AOPi
                    lzbir = aop(fid,4013,6)
                    dzbir = (suma_liste(fid,[4002,4004,4005,4006,4007],6)-suma_liste(fid,[4003,4008,4009,4010,4011,4012],6))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 4013 kol. 6 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40006
            if(suma_liste(fid,[4002,4004,4005,4006,4007],5)<suma_liste(fid,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fid,4014,5)==(suma_liste(fid,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fid,[4002,4004,4005,4006,4007],5))):
                    #AOPi
                    lzbir = aop(fid,4014,5)
                    dzbir = (suma_liste(fid,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fid,[4002,4004,4005,4006,4007],5))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 4014 kol. 5 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40007
            if(suma_liste(fid,[4002,4004,4005,4006,4007],6)<suma_liste(fid,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fid,4014,6)==(suma_liste(fid,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fid,[4002,4004,4005,4006,4007],6))):
                    #AOPi
                    lzbir = aop(fid,4014,6)
                    dzbir = (suma_liste(fid,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fid,[4002,4004,4005,4006,4007],6))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP 4014 kol. 6 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40008
            if(suma_liste(fid,[4002,4004,4005,4006,4007],5) == suma_liste(fid,[4003,4008,4009,4010,4011,4012],5)):
                if not(suma(fid,4013,4014,5)== 0):
                    #AOPi
                    lzbir = suma(fid,4013,4014,5)
                    dzbir =  0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (4013 + 4014) kol. 5 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #40009
            if(suma_liste(fid,[4002,4004,4005,4006,4007],6) == suma_liste(fid,[4003,4008,4009,4010,4011,4012],6)):
                if not(suma(fid,4013,4014,6)== 0):
                    #AOPi
                    lzbir = suma(fid,4013,4014,6)
                    dzbir =  0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    AOP (4013 + 4014) kol. 6 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,4013,5)>0):
                if not(aop(fid,4014,5)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 4013 kol. 5 > 0,onda je AOP 4014 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40011    
            if(aop(fid,4014,5)>0):
                if not(aop(fid,4013,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 4014 kol. 5 > 0,onda je AOP 4013 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fid,4013,6)>0):
                if not(aop(fid,4014,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 4013 kol. 6 > 0,onda je AOP 4014 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40013   
            if(aop(fid,4014,6)>0):
                if not(aop(fid,4013,6)==0):  
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 4'
                    poruka  ="    Ako je AOP 4014 kol. 6 > 0,onda je AOP 4013 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40014
            if not(suma_liste(fid,[4002,4004,4005,4006,4007,4014],5)==suma_liste(fid,[4003,4008,4009,4010,4011,4012,4013],5)):
                #AOPi
                lzbir = suma_liste(fid,[4002,4004,4005,4006,4007,4014],5)
                dzbir = suma_liste(fid,[4003,4008,4009,4010,4011,4012,4013],5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40015
            if not(suma_liste(fid,[4002,4004,4005,4006,4007,4014],6)==suma_liste(fid,[4003,4008,4009,4010,4011,4012,4013],6)):
                #AOPi
                lzbir = suma_liste(fid,[4002,4004,4005,4006,4007,4014],6)
                dzbir = suma_liste(fid,[4003,4008,4009,4010,4011,4012,4013],6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže;  Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40016
            if not(aop(fid,4015,5)==(suma_liste(fid,[4001,4013],5)-aop(fid,4014,5))):
                #AOPi
                lzbir = aop(fid,4015,5)
                dzbir = (suma_liste(fid,[4001,4013],5)-aop(fid,4014,5))
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4015 kol. 5 = AOP-u (4001 + 4013 - 4014) kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40017
            if not(aop(fid,4015,6)==(suma_liste(fid,[4001,4013],6)-aop(fid,4014,6))):
                #AOPi
                lzbir = aop(fid,4015,6)
                dzbir = (suma_liste(fid,[4001,4013],6)-aop(fid,4014,6))
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4015 kol. 6 = AOP-u (4001 + 4013 - 4014) kol. 6     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40018
            if not(aop(fid,4015,6)==aop(fid,4001,5)):
                #AOPi
                lzbir = aop(fid,4015,6)
                dzbir = aop(fid,4001,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 4001 kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            
            #40019
            if not(aop(fid,4001,6)==aop(fid,410,7)):
                #AOPi
                lzbir = aop(fid,4001,6)
                dzbir = aop(fid,410,7)
                razlika = lzbir - dzbir
                hasWarning=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4001 kol. 6 = AOP-u 0410 kol. 7 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40020
            if not(aop(fid,4002,5)==aop(fid,406,5)):
                #AOPi
                lzbir = aop(fid,4002,5)
                dzbir = aop(fid,406,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4002 kol. 5 = AOP-u 0406 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40021
            if not(aop(fid,4002,6)==aop(fid,406,6)):
                #AOPi
                lzbir = aop(fid,4002,6)
                dzbir = aop(fid,406,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4002 kol. 6 = AOP-u 0406 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40022
            if not(aop(fid,4003,5)==aop(fid,408,5)):
                #AOPi
                lzbir = aop(fid,4003,5)
                dzbir = aop(fid,408,5)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4003 kol. 5 = AOP-u 0408 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40023
            if not(aop(fid,4003,6)==aop(fid,408,6)):
                #AOPi
                lzbir = aop(fid,4003,6)
                dzbir = aop(fid,408,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4003 kol. 6 = AOP-u 0408 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40024
            if not(aop(fid,4015,5)==aop(fid,410,5)):
                #AOPi
                lzbir = aop(fid,4015,5)
                dzbir = aop(fid,410,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4015 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40025
            if not(aop(fid,4015,6)==aop(fid,410,6)):
                #AOPi
                lzbir = aop(fid,4015,6)
                dzbir = aop(fid,410,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 4'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND4----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND4----------------")                
                
        #############################################
        #### POCETAK KONTROLNIH PRAVILA FOND 5 ######
        #############################################
        hasWarning=False
        hasError = False      
        
        #00000
        if not(suma(fie,1,12,5) + suma(fie,401,410,5) + suma(fie,1,12,6) + suma(fie,401,410,6) + suma(fie,1,12,7) + suma(fie,401,410,7) + suma(fie,1001,1020,5) + suma(fie,1001,1020,6) + suma(fie,3001,3039,3) + suma(fie,3001,3039,4) + suma(fie,4001,4015,5) + suma(fie,4001,4015,6) > 0):
            
            naziv_obrasca='Finansijski izveštaj DPF 5'
            poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 + (0001 do 0410) kol. 6 + (0001 do 0410) kol. 7 bilansa stanja-izveštaja o neto imovini + (1001 do 1020) kol. 5 + (1001 do 1020) kol. 6 bilansa uspeha + (3001 do 3039) kol. 3 + (3001 do 3039) kol. 4 izveštaja o tokovima gotovine + (4001 do 4015) kol. 5 + (4001 do 4015) kol. 6 izveštaja o promenama na neto imovini > 0; Ukoliko podaci za FOND 1 nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga."
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
                    
        #Ako ima bar jedan unet podatak u obrazac, proveravaju se greške i upozorenja. U suprotnom se ne proveravaju
        if (suma(fie,1,12,5) + suma(fie,401,410,5) + suma(fie,1,12,6) + suma(fie,401,410,6) + suma(fie,1,12,7) + suma(fie,401,410,7) + suma(fie,1001,1020,5) + suma(fie,1001,1020,6) + suma(fie,3001,3039,3) + suma(fie,3001,3039,4) + suma(fie,4001,4015,5) + suma(fie,4001,4015,6) > 0):          

            
            naziv_obrasca='Finansijski izveštaj DPF 5'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND5----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Obrazac'
            poruka  ="----------------FINANSIJSKI IZVEŠTAJ FOND5----------------"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)

            #00001-1
            if len(Zahtev.Forme['Finansijski izveštaj DPF 5'].TekstualnaPoljaForme["aop-10101-1"])==0:
                hasError=True                
                naziv_obrasca='Obrazac'
                poruka  ="U zaglavlju obrasca, za konkretan fond potrebno je uneti njegov naziv"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00000-3 
            # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
            fieNapomene = Zahtev.Forme['Finansijski izveštaj DPF 1'].TekstualnaPoljaForme;

            if not(proveriNapomene(fieNapomene, 1, 12, 4) or proveriNapomene(fieNapomene, 401, 410, 4) or proveriNapomene(fieNapomene, 1001, 1020, 4) or proveriNapomene(fieNapomene, 4001, 4015, 4)):
                hasError = True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="Na AOP-u (0001 do 0012) bilansa stanja-izveštaja o neto imovini + (0401 do 0410) bilansa stanja-izveštaja o neto imovini + (1001 do 1020) bilansa uspeha + (4001 do 4015) izveštaja o promenama na neto imovini u koloni 4 (Napomena) mora biti unet bar jedan karakter; Potrebno je popuniti kolonu 4 u skladu sa oznakama iz Napomena uz finansijske izveštaje"
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00001
            if not((suma(fie,1,12,5)+suma(fie,401,410,5))>0):
                hasWarning=True                
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 5 > 0; Bilans stanja,po pravilu,mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "    
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #00002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fie,1,12,6)+suma(fie,401,410,6))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 = 0; Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00003
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not((suma(fie,1,12,7)+suma(fie,401,410,7))==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 7 + (0401 do 0410) kol. 7 = 0;Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00004			
            if(Zahtev.ObveznikInfo.Novoosnovan ==False):
                if not((suma(fie,1,12,6)+suma(fie,401,410,6))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0012) kol. 6 + (0401 do 0410) kol. 6 > 0 ; Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga   "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00005
            if(Zahtev.ObveznikInfo.Novoosnovan== False):
                if not((suma(fie,1,12,7)+suma(fie,401,410,7))>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ="    Zbir podataka na oznakama za AOP (0001 do 0410) kol. 7 > 0; Bilans stanja,po pravilu, mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju;Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #00006
            if not(aop(fie,12,5)==suma(fie,1,11,5)):
                #AOPi
                lzbir =   aop(fie,12,5)
                dzbir =   suma(fie,1,11,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00007
            if not(aop(fie,12,6)==suma(fie,1,11,6)):
                #AOPi
                lzbir =   aop(fie,12,6)
                dzbir =   suma(fie,1,11,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00008
            if not(aop(fie,12,7)==suma(fie,1,11,7)):
                #AOPi
                lzbir =   aop(fie,12,7)
                dzbir =   suma(fie,1,11,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0012 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0005 + 0006 + 0007 + 0008 + 0009 + 0010 + 0011) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00009
            if not(aop(fie,404,5)== suma(fie,401,403,5)):
                #AOPi
                lzbir =   aop(fie,404,5)
                dzbir =   suma(fie,401,403,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 5 = AOP-u (0401 + 0402 + 0403) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00010
            if not(aop(fie,404,6)== suma(fie,401,403,6)):
                #AOPi
                lzbir =   aop(fie,404,6)
                dzbir =   suma(fie,401,403,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 6 = AOP-u (0401 + 0402 + 0403) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00011
            if not(aop(fie,404,7)==suma(fie,401,403,7)):
                #AOPi
                lzbir =   aop(fie,404,7)
                dzbir =   suma(fie,401,403,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0404 kol. 7 = AOP-u (0401 + 0402 + 0403) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00012
            if not(aop(fie,410,5)==(suma(fie,405,407,5)-suma(fie,408,409,5))):
                #AOPi
                lzbir =   aop(fie,410,5)
                dzbir =   (suma(fie,405,407,5)-suma(fie,408,409,5))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 5        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00013
            if not(aop(fie,410,6)==(suma(fie,405,407,6)-suma(fie,408,409,6))):
                #AOPi
                lzbir =   aop(fie,410,6)
                dzbir =   (suma(fie,405,407,6)-suma(fie,408,409,6))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 6        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00014
            if not(aop(fie,410,7)==(suma(fie,405,407,7)-suma(fie,408,409,7))):
                #AOPi
                lzbir =   aop(fie,410,7)
                dzbir =   (suma(fie,405,407,7)-suma(fie,408,409,7))
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 7 = AOP-u (0405 + 0406 + 0407 - 0408 - 0409) kol. 7        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00015
            if not(aop(fie,410,5)==aop(fie,12,5)-aop(fie,404,5)):
                #AOPi
                lzbir =   aop(fie,410,5)
                dzbir =   aop(fie,12,5)-aop(fie,404,5)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 5 = AOP-u (0012 - 0404) kol. 5; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00016
            if not(aop(fie,410,6)==aop(fie,12,6)-aop(fie,404,6)):
                #AOPi
                lzbir =   aop(fie,410,6)
                dzbir =   aop(fie,12,6)-aop(fie,404,6)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 0410 kol. 6 = AOP-u (0012 - 0404) kol. 6; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #00017
            if not(aop(fie,410,7) == aop(fie,12,7)-aop(fie,404,7)):
                #AOPi
                lzbir =   aop(fie,410,7) 
                dzbir =    aop(fie,12,7)-aop(fie,404,7)
                razlika = lzbir - dzbir        
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="   AOP 0410 kol. 7 = AOP-u (0012 - 0404) kol. 7; Kontrolno pravilo zahteva jednakost neto imovine raspoložive za penzije i razlike između ukupne imovine i ukupnih obaveza        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #10001
            if not(suma(fie,1001,1020,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 5 > 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #10002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fie,1001,1020,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 = 0; Bilans uspeha,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fie,1001,1020,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans uspeha'
                    poruka  ="    Zbir podataka na oznakama za AOP (1001 do 1020) kol. 6 > 0; Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #10004 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1001,5)>0):
                if not(aop(fie,1002,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1001 kol. 5 > 0, onda je AOP 1002 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10005
            if(aop(fie,1002,5)>0):
                if not(aop(fie,1001,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="     Ako je AOP 1002 kol. 5 > 0, onda je AOP 1001 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10006 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1001,6)>0):
                if not(aop(fie,1002,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1001 kol. 6 > 0,onda je AOP 1002 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10007
            if(aop(fie,1002,6)>0):
                if not(aop(fie,1001,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1002 kol. 6 > 0,onda je AOP 1001 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10008 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1003,5)>0):
                if not(aop(fie,1004,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1003 kol. 5 > 0,onda je AOP 1004 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10009
            if(aop(fie,1004,5)>0):
                if not(aop(fie,1003,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1004 kol. 5 > 0,onda je AOP 1003 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1003,6)>0):
                if not(aop(fie,1004,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1003 kol. 6 > 0,onda je AOP 1004 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10011
            if(aop(fie,1004,6)>0):
                if not(aop(fie,1003,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1004 kol. 6 > 0,onda je AOP 1003 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1005,5)>0):
                if not(aop(fie,1006,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1005 kol. 5 > 0,onda je AOP 1006 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10013
            if(aop(fie,1006,5)>0):
                if not(aop(fie,1005,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1006 kol. 5 > 0,onda je AOP 1005 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1005,6)>0):
                if not(aop(fie,1006,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1005 kol. 6 > 0,onda je AOP 1006 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10015
            if(aop(fie,1006,6)>0):
                if not(aop(fie,1005,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Ako je AOP 1006 kol. 6 > 0,onda je AOP 1005 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazane neto pozitivne kursne razlike i neto negativne kursne razlike     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1007,5)>0):
                if not(aop(fie,1008,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1007 kol. 5 > 0,onda je AOP 1008 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10017
            if(aop(fie,1008,5)>0):
                if not(aop(fie,1007,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1008 kol. 5 > 0,onda je AOP 1007 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10018 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1007,6)>0):
                if not(aop(fie,1008,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1007 kol. 6 > 0,onda je AOP 1008 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10019
            if(aop(fie,1008,6)>0):
                if not(aop(fie,1007,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1008 kol. 6 > 0,onda je AOP 1007 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10020 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1009,5)>0):
                if not(aop(fie,1010,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 5 > 0,onda je AOP 1010 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10021
            if(aop(fie,1010,5)>0):
                if not(aop(fie,1009,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1010 kol. 5 > 0,onda je AOP 1009 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10022 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1009,6)>0):
                if not(aop(fie,1010,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10023
            if(aop(fie,1010,6)>0):
                if not(aop(fie,1009,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1009 kol. 6 > 0,onda je AOP 1010 kol. 6 = 0,i obrnuto,ako je AOP 1010 kol. 6 > 0,onda je AOP 1009 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10024
            if(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)>suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)):
                if not(aop(fie,1019,5)==(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                    #AOPi
                    lzbir = aop(fie,1019,5)
                    dzbir = (suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1019 kol. 5 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #10025
            if(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)>suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)):
                if not(aop(fie,1019,6)==(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                    #AOPi
                    lzbir = aop(fie,1019,6)
                    dzbir = (suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)-suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1019 kol. 6 = AOP-u (1001 - 1002 + 1003 - 1004 + 1005 - 1006 + 1007 - 1008 + 1009 - 1010 + 1011 + 1012 + 1013 + 1014 - 1015 - 1016 - 1017 - 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 > AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10026
            if(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)>suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)):
                if not(aop(fie,1020,5)==(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))):
                    #AOPi
                    lzbir = aop(fie,1020,5)
                    dzbir = (suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1020 kol. 5 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 5, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10027
            if(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)>suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)):
                if not(aop(fie,1020,6)==(suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))):
                    #AOPi
                    lzbir = aop(fie,1020,6)
                    dzbir = (suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6)-suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 1020 kol. 6 = AOP-u (1002 - 1001 - 1003 + 1004 - 1005 + 1006 - 1007 + 1008 - 1009 + 1010 - 1011 - 1012 - 1013 - 1014 + 1015 + 1016 + 1017 + 1018) kol. 6, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 < AOP-a (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10028
            if((suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],5)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],5))):
                if not(suma(fie,1019,1020,5)==0):
                    #AOPi
                    lzbir = suma(fie,1019,1020,5)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (1019 + 1020) kol. 5 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10029
            if((suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014],6)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018],6))):
                if not(suma(fie,1019,1020,6)==0):
                    #AOPi
                    lzbir = suma(fie,1019,1020,6)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (1019 + 1020) kol. 6 = 0, ako je AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1019,5)>0):
                if not(aop(fie,1020,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1019 kol. 5 > 0,onda je AOP 1020 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10031            
            if(aop(fie,1020,5)>0):
                if not(aop(fie,1019,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1020 kol. 5 > 0,onda je AOP 1019 kol. 5 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,1019,6)>0):
                if not(aop(fie,1020,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1019 kol. 6 > 0,onda je AOP 1020 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #10033         
            if(aop(fie,1020,6)>0):
                if not(aop(fie,1019,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 1020 kol. 6 > 0,onda je AOP 1019 kol. 6 = 0; U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                        
            #10034
            if not(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)):
                #AOPi
                lzbir = suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],5)
                dzbir = suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],5)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 5 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                    
            #10035
            if not(suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)==suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)):
                #AOPi
                lzbir = suma_liste(fie,[1001,1003,1005,1007,1009,1011,1012,1013,1014,1020],6)
                dzbir = suma_liste(fie,[1002,1004,1006,1008,1010,1015,1016,1017,1018,1019],6)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (1001 + 1003 + 1005 + 1007 + 1009 + 1011 + 1012 + 1013 + 1014 + 1020) kol. 6 = AOP-u (1002 + 1004 + 1006 + 1008 + 1010 + 1015 + 1016 + 1017 + 1018 + 1019) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

                
            #30001
            if not(suma(fie,3001,3039,3)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 3 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #30002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(suma(fie,3001,3039,4)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 = 0; Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):
                if not(suma(fie,3001,3039,4)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Izveštaj o tokovima gotovine'
                    poruka  ="    Zbir podataka na oznakama za AOP (3001 do 3039) kol. 4 > 0; Izveštaj o tokovima gotovine,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #30004
            if not(aop(fie,3001,3)==suma_liste(fie,[3002,3003,3004,3005,3006,3007,3008],3)):
                #AOPi
                lzbir = aop(fie,3001,3)
                dzbir = suma_liste(fie,[3002,3003,3004,3005,3006,3007,3008],3)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3001 kol. 3 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30005
            if not(aop(fie,3001,4)==suma_liste(fie,[3002,3003,3004,3005,3006,3007,3008],4)):
                #AOPi
                lzbir = aop(fie,3001,4)
                dzbir = suma_liste(fie,[3002,3003,3004,3005,3006,3007,3008],4)
                razlika = lzbir - dzbir
                hasError=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3001 kol. 4 = AOP-u (3002 + 3003 + 3004 + 3005 + 3006 + 3007 + 3008) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30006
            if not(aop(fie,3009,3)==suma_liste(fie,[3010,3011,3012,3013,3014,3015,3016],3)):
                #AOPi
                lzbir = aop(fie,3009,3)
                dzbir = suma_liste(fie,[3010,3011,3012,3013,3014,3015,3016],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3009 kol. 3 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30007
            if not(aop(fie,3009,4)==suma_liste(fie,[3010,3011,3012,3013,3014,3015,3016],4)):
                #AOPi
                lzbir = aop(fie,3009,4)
                dzbir = suma_liste(fie,[3010,3011,3012,3013,3014,3015,3016],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3009 kol. 4 = AOP-u (3010 + 3011 + 3012 + 3013 + 3014 + 3015 + 3016) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30008
            if(aop(fie,3001,3)>aop(fie,3009,3)):
                if not(aop(fie,3017,3)==(aop(fie,3001,3)-aop(fie,3009,3))):
                    #AOPi
                    lzbir = aop(fie,3017,3)
                    dzbir = (aop(fie,3001,3)-aop(fie,3009,3))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP 3017 kol. 3 = AOP-u (3001 - 3009) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3009 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30009
            if(aop(fie,3001,4)>aop(fie,3009,4)):
                if not(aop(fie,3017,4)==(aop(fie,3001,4)-aop(fie,3009,4))):
                    #AOPi
                    lzbir = aop(fie,3017,4)
                    dzbir = (aop(fie,3001,4)-aop(fie,3009,4))
                    razlika = lzbir - dzbir
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3017 kol. 4 = AOP-u (3001 - 3009) kol. 4, ako je AOP 3001 kol. 4 > AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30010
            if(aop(fie,3001,3)<aop(fie,3009,3)):
                if not(aop(fie,3018,3)==(aop(fie,3009,3)-aop(fie,3001,3))):
                    #AOPi
                    lzbir = aop(fie,3018,3)
                    dzbir = (aop(fie,3009,3)-aop(fie,3001,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3018 kol. 3 = AOP-u (3009 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3009 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30011
            if(aop(fie,3001,4)<aop(fie,3009,4)):
                if not(aop(fie,3018,4)==(aop(fie,3009,4)-aop(fie,3001,4))):
                    #AOPi
                    lzbir = aop(fie,3018,4)
                    dzbir = (aop(fie,3009,4)-aop(fie,3001,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3018 kol. 4 = AOP-u (3009 - 3001) kol. 4,ako je AOP 3001 kol. 4 < AOP-a 3009 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30012
            if(aop(fie,3001,3)==aop(fie,3009,3)):
                if not(suma(fie,3017,3018,3)==0):
                    #AOPi
                    lzbir = suma(fie,3017,3018,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (3017 + 3018) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3009 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30013
            if(aop(fie,3001,4)==aop(fie,3009,4)):
                if not(suma(fie,3017,3018,4)==0):
                    #AOPi
                    lzbir = suma(fie,3017,3018,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True        
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP (3017 + 3018) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3009 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                   
            #30014 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3017,3)>0):
                if not(aop(fie,3018,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3017 kol. 3 > 0,onda je AOP 3018 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30015
            if(aop(fie,3018,3)>0):
                if not(aop(fie,3017,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3018 kol. 3 > 0,onda je AOP 3017 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30016 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3017,4)>0):
                if not(aop(fie,3018,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3017 kol. 4 > 0,onda je AOP 3018 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30017
            if(aop(fie,3018,4)>0):
                if not(aop(fie,3017,4)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3018 kol. 4 > 0,onda je AOP 3017 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30018
            if not(suma_liste(fie,[3001,3018],3)==suma_liste(fie,[3009,3017],3)):
                #AOPi
                lzbir = suma_liste(fie,[3001,3018],3)
                dzbir = suma_liste(fie,[3009,3017],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3001 + 3018) kol. 3 = AOP-u (3009 + 3017) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30019
            if not(suma_liste(fie,[3001,3018],4)==suma_liste(fie,[3009,3017],4)):
                #AOPi
                lzbir = suma_liste(fie,[3001,3018],4)
                dzbir = suma_liste(fie,[3009,3017],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3001 + 3018) kol. 4 = AOP-u (3009 + 3017) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30020
            if not(aop(fie,3019,3)==suma(fie,3020,3023,3)):
                #AOPi
                lzbir = aop(fie,3019,3)
                dzbir = suma(fie,3020,3023,3)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3019 kol. 3 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30021
            if not(aop(fie,3019,4)==suma(fie,3020,3023,4)):
                #AOPi
                lzbir = aop(fie,3019,4)
                dzbir = suma(fie,3020,3023,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3019 kol. 4 = AOP-u (3020 + 3021 + 3022 + 3023) kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30022
            if not(aop(fie,3024,3)==suma(fie,3025,3029,3)):
                #AOPi
                lzbir = aop(fie,3024,3)
                dzbir = suma(fie,3025,3029,3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3024 kol. 3 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30023
            if not(aop(fie,3024,4)==suma(fie,3025,3029,4)):
                #AOPi
                lzbir = aop(fie,3024,4)
                dzbir = suma(fie,3025,3029,4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3024 kol. 4 = AOP-u (3025 + 3026 + 3027 + 3028 + 3029) kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30024
            if(aop(fie,3019,3)>aop(fie,3024,3)):
                if not(aop(fie,3030,3)==(aop(fie,3019,3)-aop(fie,3024,3))):
                    #AOPi
                    lzbir = aop(fie,3030,3)
                    dzbir = (aop(fie,3019,3)-aop(fie,3024,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP 3030 kol. 3 = AOP-u (3019 - 3024) kol. 3, ako je AOP 3019 kol. 3 > AOP-a 3024 kol. 3       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30025
            if(aop(fie,3019,4)>aop(fie,3024,4)):
                if not(aop(fie,3030,4)==(aop(fie,3019,4)-aop(fie,3024,4))):
                    #AOPi
                    lzbir = aop(fie,3030,4)
                    dzbir = (aop(fie,3019,4)-aop(fie,3024,4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3030 kol. 4 = AOP-u (3019 - 3024) kol. 4, ako je AOP 3019 kol. 4 > AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30026
            if(aop(fie,3019,3)<aop(fie,3024,3)):
                if not(aop(fie,3031,3)==(aop(fie,3024,3)-aop(fie,3019,3))):
                    #AOPi
                    lzbir = aop(fie,3031,3)
                    dzbir = (aop(fie,3024,3)-aop(fie,3019,3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3031 kol. 3 = AOP-u (3024 - 3019) kol. 3, ako je AOP 3019 kol. 3 < AOP-a 3024 kol. 3        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30027
            if(aop(fie,3019,4)<aop(fie,3024,4)):
                if not(aop(fie,3031,4)==(aop(fie,3024,4)-aop(fie,3019,4))):
                    #AOPi
                    lzbir = aop(fie,3031,4)
                    dzbir = (aop(fie,3024,4)-aop(fie,3019,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3031 kol. 4 = AOP-u (3024 - 3019) kol. 4, ako je AOP 3019 kol. 4 < AOP-a 3024 kol. 4        "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30028
            if(aop(fie,3019,3)==aop(fie,3024,3)):
                if not(suma(fie,3030,3031,3)==0):
                    #AOPi
                    lzbir = suma(fie,3030,3031,3)
                    dzbir = 0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP (3030 + 3031) kol. 3 = 0, ako je AOP 3019 kol. 3 = AOP-u 3024 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30029
            if(aop(fie,3019,4)==aop(fie,3024,4)):
                if not(suma(fie,3030,3031,4)==0):
                    #AOPi
                    lzbir = suma(fie,3030,3031,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (3030 + 3031) kol. 4 = 0, ako je AOP 3019 kol. 4 = AOP-u 3024 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30030 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3030,3)>0):
                if not(aop(fie,3031,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3030 kol. 3 > 0,onda je AOP 3031 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30031
            if(aop(fie,3031,3)>0):
                if not(aop(fie,3030,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3031 kol. 3 > 0,onda je AOP 3030 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30032 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3030,4)>0):
                if not(aop(fie,3031,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   Ako je AOP 3030 kol. 4 > 0,onda je AOP 3031 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30033
            if(aop(fie,3031,4)>0):
                if not(aop(fie,3030,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   Ako je AOP 3031 kol. 4 > 0,onda je AOP 3030 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #30034
            if not(suma_liste(fie,[3019,3031],3)==suma_liste(fie,[3024,3030],3)):
                #AOPi
                lzbir = suma_liste(fie,[3019,3031],3)
                dzbir = suma_liste(fie,[3024,3030],3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3019 + 3031) kol. 3 = AOP-u (3024 + 3030) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30035
            if not(suma_liste(fie,[3019,3031],4)==suma_liste(fie,[3024,3030],4)):
                #AOPi
                lzbir = suma_liste(fie,[3019,3031],4)
                dzbir = suma_liste(fie,[3024,3030],4)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3019 + 3031) kol. 4 = AOP-u (3024 + 3030) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)

            #30036
            if not(aop(fie,3032,3)==suma_liste(fie,[3017,3030],3)):
                #AOPi
                lzbir = aop(fie,3032,3)
                dzbir = suma_liste(fie,[3017,3030],3)
                razlika = lzbir - dzbir     
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3032 kol. 3 = AOP-u (3017 + 3030) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30037
            if not(aop(fie,3032,4)==suma_liste(fie,[3017,3030],4)):
                #AOPi
                lzbir = aop(fie,3032,4)
                dzbir = suma_liste(fie,[3017,3030],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3032 kol. 4 = AOP-u (3017 + 3030) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30038
            if not(aop(fie,3033,3)==suma_liste(fie,[3018,3031],3)):
                #AOPi
                lzbir = aop(fie,3033,3)
                dzbir = suma_liste(fie,[3018,3031],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="   AOP 3033 kol. 3 = AOP-u (3018 + 3031) kol. 3     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30039
            if not(aop(fie,3033,4)==suma_liste(fie,[3018,3031],4)):
                #AOPi
                lzbir = aop(fie,3033,4)
                dzbir = suma_liste(fie,[3018,3031],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="   AOP 3033 kol. 4 = AOP-u (3018 + 3031) kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30040
            if(aop(fie,3032,3)>aop(fie,3033,3)):
                if not(aop(fie,3034,3)==(aop(fie,3032,3)-aop(fie,3033,3))):
                    #AOPi
                    lzbir = aop(fie,3034,3)
                    dzbir = (aop(fie,3032,3)-aop(fie,3033,3))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3034 kol. 3 = AOP-u (3032 - 3033) kol. 3, ako je AOP 3032 kol. 3 > AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30041
            if(aop(fie,3032,4)>aop(fie,3033,4)):
                if not(aop(fie,3034,4)==(aop(fie,3032,4)-aop(fie,3033,4))):
                    #AOPi
                    lzbir = aop(fie,3034,4)
                    dzbir = (aop(fie,3032,4)-aop(fie,3033,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP 3034 kol. 4 = AOP-u (3032 - 3033) kol. 4, ako je AOP 3032 kol. 4 > AOP-a 3033 kol. 4      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30042
            if(aop(fie,3032,3)<aop(fie,3033,3)):
                if not(aop(fie,3035,3)==(aop(fie,3033,3)-aop(fie,3032,3))):
                    #AOPi
                    lzbir = aop(fie,3035,3)
                    dzbir = (aop(fie,3033,3)-aop(fie,3032,3))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3035 kol. 3 = AOP-u (3033 - 3032) kol. 3, ako je AOP 3032 kol. 3 < AOP-a 3033 kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30043    
            if(aop(fie,3032,4)<aop(fie,3033,4)):
                if not(aop(fie,3035,4)==(aop(fie,3033,4)-aop(fie,3032,4))):
                    #AOPi
                    lzbir = aop(fie,3035,4)
                    dzbir = (aop(fie,3033,4)-aop(fie,3032,4))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3035 kol. 4 = AOP-u (3033 - 3032) kol. 4, ako je AOP 3032 kol. 4 < AOP-a 3033 kol. 4       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30044    
            if(aop(fie,3032,3)==aop(fie,3033,3)):
                if not(suma(fie,3034,3035,3)==0):
                    #AOPi
                    lzbir = suma(fie,3034,3035,3)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (3034 + 3035) kol. 3 = 0, ako je AOP 3032 kol. 3 = AOP-u 3033 kol. 3; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30045    
            if(aop(fie,3032,4)==aop(fie,3033,4)):
                if not(suma(fie,3034,3035,4)==0):
                    #AOPi
                    lzbir = suma(fie,3034,3035,4)
                    dzbir = 0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP (3034 + 3035) kol. 4 = 0, ako je AOP 3032 kol. 4 = AOP-u 3033 kol. 4; Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30046 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3034,3)>0):
                if not(aop(fie,3035,3)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3034 kol. 3 > 0,onda je AOP 3035 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30047    
            if(aop(fie,3035,3)>0):
                if not(aop(fie,3034,3)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3035 kol. 3 > 0,onda je AOP 3034 kol. 3 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30048 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,3034,4)>0):
                if not(aop(fie,3035,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #30049
            if(aop(fie,3035,4)>0):
                if not(aop(fie,3034,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 3034 kol. 4 > 0,onda je AOP 3035 kol. 4 = 0,i obrnuto,ako je AOP 3035 kol. 4 > 0,onda je AOP 3034 kol. 4 = 0; U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #30050
            if not(suma_liste(fie,[3032,3035],3)==suma_liste(fie,[3033,3034],3)):
                #AOPi
                lzbir = suma_liste(fie,[3032,3035],3)
                dzbir = suma_liste(fie,[3033,3034],3)
                razlika = lzbir - dzbir  
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3032 + 3035) kol. 3 = AOP-u (3033 + 3034) kol. 3; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30051
            if not(suma_liste(fie,[3032,3035],4)==suma_liste(fie,[3033,3034],4)):
                #AOPi
                lzbir = suma_liste(fie,[3032,3035],4)
                dzbir = suma_liste(fie,[3033,3034],4)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (3032 + 3035) kol. 4 = AOP-u (3033 + 3034) kol. 4; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #30052
            if(Zahtev.ObveznikInfo.Novoosnovan == True):
                if not(aop(fie,3036,3)==0):
                    hasWarning=True 
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3036 kol. 3 = 0; Novoosnovana pravna lica po pravilu ne smeju imati prikazan podatak za prethodnu godinu "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                
            #30053
            if(suma_liste(fie,[3034,3036,3037],3)>suma_liste(fie,[3035,3038],3)):
                if not(aop(fie,3039,3)==(suma_liste(fie,[3034,3036,3037],3)-suma_liste(fie,[3035,3038],3))):
                    #AOPi
                    lzbir = aop(fie,3039,3)
                    dzbir = (suma_liste(fie,[3034,3036,3037],3)-suma_liste(fie,[3035,3038],3))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP 3039 kol. 3 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 3, ako je AOP (3034 + 3036 + 3037) kol. 3 > AOP-a (3035 + 3038) kol. 3      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30054
            if(suma_liste(fie,[3034,3036,3037],4)>suma_liste(fie,[3035,3038],4)):
                if not(aop(fie,3039,4)==(suma_liste(fie,[3034,3036,3037],4)-suma_liste(fie,[3035,3038],4))):
                    #AOPi
                    lzbir = aop(fie,3039,4)
                    dzbir = (suma_liste(fie,[3034,3036,3037],4)-suma_liste(fie,[3035,3038],4))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="   AOP 3039 kol. 4 = AOP-u (3034 - 3035 + 3036 + 3037 - 3038) kol. 4, ako je AOP (3034 + 3036 + 3037) kol. 4 > AOP-a (3035 + 3038) kol. 4     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30055
            if(suma_liste(fie,[3034,3036,3037],3)<=suma_liste(fie,[3035,3038],3)):
                if not(aop(fie,3039,3)==0):   
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3039 kol. 3 = 0, ako je AOP (3034 + 3036 + 3037) kol. 3 ≤ AOP-a (3035 + 3038) kol. 3 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                    
            #30056
            if(suma_liste(fie,[3034,3036,3037],4)<=suma_liste(fie,[3035,3038],4)):
                if not(aop(fie,3039,4)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 3039 kol. 4 = 0, ako je AOP (3034 + 3036 + 3037) kol. 4 ≤ AOP-a (3035 + 3038) kol. 4 "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #30057
            if not(aop(fie,3039,4)==aop(fie,3036,3)):
                #AOPi
                lzbir = aop(fie,3039,4)
                dzbir = aop(fie,3036,3)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 3036 kol. 3   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
                
            #30058
            if not(aop(fie,3039,3)==aop(fie,1,5)):
                #AOPi
                lzbir = aop(fie,3039,3)
                dzbir = aop(fie,1,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3039 kol. 3 = AOP-u 0001 kol. 5 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                
            #30059
            if not(aop(fie,3039,4)==aop(fie,1,6)):
                #AOPi
                lzbir = aop(fie,3039,4)
                dzbir = aop(fie,1,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 3039 kol. 4 = AOP-u 0001 kol. 6 bilansa stanja; Računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju, po pravilu  treba da postoji; Ukoliko su uneti podaci tačni, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40001    
            if not(suma(fie,4001,4015,5)>0):
                hasWarning=True
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 5 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga  "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)

            #40002
            if(Zahtev.ObveznikInfo.Novoosnovan == True):    
                if not(suma(fie,4001,4015,6)==0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 = 0; Izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; Ukoliko su podaci prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)

            #40003
            if(Zahtev.ObveznikInfo.Novoosnovan == False):    
                if not(suma(fie,4001,4015,6)>0):
                    hasWarning=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="  Zbir podataka na oznakama za AOP (4001 do 4015) kol. 6 > 0; Izveštaj o promenama na neto imovini,po pravilu, mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani,zakonski zastupnik svojim potpisom potvrđuje ispravnost toga    "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
            
            #40004
            if(suma_liste(fie,[4002,4004,4005,4006,4007],5)>suma_liste(fie,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fie,4013,5)==(suma_liste(fie,[4002,4004,4005,4006,4007],5)-suma_liste(fie,[4003,4008,4009,4010,4011,4012],5))):
                    #AOPi
                    lzbir = aop(fie,4013,5)
                    dzbir = (suma_liste(fie,[4002,4004,4005,4006,4007],5)-suma_liste(fie,[4003,4008,4009,4010,4011,4012],5))
                    razlika = lzbir - dzbir  
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 4013 kol. 5 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
                
            #40005
            if(suma_liste(fie,[4002,4004,4005,4006,4007],6)>suma_liste(fie,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fie,4013,6)==(suma_liste(fie,[4002,4004,4005,4006,4007],6)-suma_liste(fie,[4003,4008,4009,4010,4011,4012],6))):
                    #AOPi
                    lzbir = aop(fie,4013,6)
                    dzbir = (suma_liste(fie,[4002,4004,4005,4006,4007],6)-suma_liste(fie,[4003,4008,4009,4010,4011,4012],6))
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 4013 kol. 6 = AOP-u (4002 - 4003 + 4004 + 4005 + 4006 + 4007 - 4008 - 4009 - 4010 - 4011 - 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 > AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6      "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40006
            if(suma_liste(fie,[4002,4004,4005,4006,4007],5)<suma_liste(fie,[4003,4008,4009,4010,4011,4012],5)):
                if not(aop(fie,4014,5)==(suma_liste(fie,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fie,[4002,4004,4005,4006,4007],5))):
                    #AOPi
                    lzbir = aop(fie,4014,5)
                    dzbir = (suma_liste(fie,[4003,4008,4009,4010,4011,4012],5)-suma_liste(fie,[4002,4004,4005,4006,4007],5))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 4014 kol. 5 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 5, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40007
            if(suma_liste(fie,[4002,4004,4005,4006,4007],6)<suma_liste(fie,[4003,4008,4009,4010,4011,4012],6)):
                if not(aop(fie,4014,6)==(suma_liste(fie,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fie,[4002,4004,4005,4006,4007],6))):
                    #AOPi
                    lzbir = aop(fie,4014,6)
                    dzbir = (suma_liste(fie,[4003,4008,4009,4010,4011,4012],6)-suma_liste(fie,[4002,4004,4005,4006,4007],6))
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP 4014 kol. 6 = AOP-u (4003 - 4002 - 4004 - 4005 - 4006 - 4007 + 4008 + 4009 + 4010 + 4011+ 4012) kol. 6, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 < AOP-a (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6       "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40008
            if(suma_liste(fie,[4002,4004,4005,4006,4007],5) == suma_liste(fie,[4003,4008,4009,4010,4011,4012],5)):
                if not(suma(fie,4013,4014,5)== 0):
                    #AOPi
                    lzbir = suma(fie,4013,4014,5)
                    dzbir =  0
                    razlika = lzbir - dzbir 
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (4013 + 4014) kol. 5 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 5; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)

            #40009
            if(suma_liste(fie,[4002,4004,4005,4006,4007],6) == suma_liste(fie,[4003,4008,4009,4010,4011,4012],6)):
                if not(suma(fie,4013,4014,6)== 0):
                    #AOPi
                    lzbir = suma(fie,4013,4014,6)
                    dzbir =  0
                    razlika = lzbir - dzbir
                    hasError=True    
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    AOP (4013 + 4014) kol. 6 = 0, ako je AOP (4002 + 4004 + 4005 + 4006 + 4007) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012) kol. 6; Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake   "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40010 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,4013,5)>0):
                if not(aop(fie,4014,5)==0): 
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 4013 kol. 5 > 0,onda je AOP 4014 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40011    
            if(aop(fie,4014,5)>0):
                if not(aop(fie,4013,5)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 4014 kol. 5 > 0,onda je AOP 4013 kol. 5 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40012 - Ovo pravilo se prakticno sastoji od dva pravila,koja su zbog citljivosti koda razdvojena
            if(aop(fie,4013,6)>0):
                if not(aop(fie,4014,6)==0):
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 4013 kol. 6 > 0,onda je AOP 4014 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            #40013   
            if(aop(fie,4014,6)>0):
                if not(aop(fie,4013,6)==0):  
                    hasError=True
                    
                    naziv_obrasca='Finansijski izveštaj DPF 5'
                    poruka  ="    Ako je AOP 4014 kol. 6 > 0,onda je AOP 4013 kol. 6 = 0; U Izveštaju o promenama na neto imovini ne mogu biti istovremeno prikazana neto povećanja i smanjenja "
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_errors.append(poruka_obrasca)
            
            #40014
            if not(suma_liste(fie,[4002,4004,4005,4006,4007,4014],5)==suma_liste(fie,[4003,4008,4009,4010,4011,4012,4013],5)):
                #AOPi
                lzbir = suma_liste(fie,[4002,4004,4005,4006,4007,4014],5)
                dzbir = suma_liste(fie,[4003,4008,4009,4010,4011,4012,4013],5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 5 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 5; Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40015
            if not(suma_liste(fie,[4002,4004,4005,4006,4007,4014],6)==suma_liste(fie,[4003,4008,4009,4010,4011,4012,4013],6)):
                #AOPi
                lzbir = suma_liste(fie,[4002,4004,4005,4006,4007,4014],6)
                dzbir = suma_liste(fie,[4003,4008,4009,4010,4011,4012,4013],6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP (4002 + 4004 + 4005 + 4006 + 4007 + 4014) kol. 6 = AOP-u (4003 + 4008 + 4009 + 4010 + 4011 + 4012 + 4013) kol. 6; Kontrolno pravilo odražava princip bilansne ravnoteže;  Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40016
            if not(aop(fie,4015,5)==(suma_liste(fie,[4001,4013],5)-aop(fie,4014,5))):
                #AOPi
                lzbir = aop(fie,4015,5)
                dzbir = (suma_liste(fie,[4001,4013],5)-aop(fie,4014,5))
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4015 kol. 5 = AOP-u (4001 + 4013 - 4014) kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40017
            if not(aop(fie,4015,6)==(suma_liste(fie,[4001,4013],6)-aop(fie,4014,6))):
                #AOPi
                lzbir = aop(fie,4015,6)
                dzbir = (suma_liste(fie,[4001,4013],6)-aop(fie,4014,6))
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4015 kol. 6 = AOP-u (4001 + 4013 - 4014) kol. 6     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40018
            if not(aop(fie,4015,6)==aop(fie,4001,5)):
                #AOPi
                lzbir = aop(fie,4015,6)
                dzbir = aop(fie,4001,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 4001 kol. 5     "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            
            #40019
            if not(aop(fie,4001,6)==aop(fie,410,7)):
                #AOPi
                lzbir = aop(fie,4001,6)
                dzbir = aop(fie,410,7)
                razlika = lzbir - dzbir
                hasWarning=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4001 kol. 6 = AOP-u 0410 kol. 7 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju; ovo pravilo primenjuju obveznici koji vrše reklasifikaciju  "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
            
            #40020
            if not(aop(fie,4002,5)==aop(fie,406,5)):
                #AOPi
                lzbir = aop(fie,4002,5)
                dzbir = aop(fie,406,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4002 kol. 5 = AOP-u 0406 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40021
            if not(aop(fie,4002,6)==aop(fie,406,6)):
                #AOPi
                lzbir = aop(fie,4002,6)
                dzbir = aop(fie,406,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4002 kol. 6 = AOP-u 0406 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40022
            if not(aop(fie,4003,5)==aop(fie,408,5)):
                #AOPi
                lzbir = aop(fie,4003,5)
                dzbir = aop(fie,408,5)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4003 kol. 5 = AOP-u 0408 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40023
            if not(aop(fie,4003,6)==aop(fie,408,6)):
                #AOPi
                lzbir = aop(fie,4003,6)
                dzbir = aop(fie,408,6)
                razlika = lzbir - dzbir
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4003 kol. 6 = AOP-u 0408 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40024
            if not(aop(fie,4015,5)==aop(fie,410,5)):
                #AOPi
                lzbir = aop(fie,4015,5)
                dzbir = aop(fie,410,5)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4015 kol. 5 = AOP-u 0410 kol. 5 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            
            #40025
            if not(aop(fie,4015,6)==aop(fie,410,6)):
                #AOPi
                lzbir = aop(fie,4015,6)
                dzbir = aop(fie,410,6)
                razlika = lzbir - dzbir 
                hasError=True    
                
                naziv_obrasca='Finansijski izveštaj DPF 5'
                poruka  ="    AOP 4015 kol. 6 = AOP-u 0410 kol. 6 bilansa stanja; Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju    "  +  "(Levi zbir= " + str(lzbir) + ", Desni zbir= " + str(dzbir) + ", Razlika= " + str(razlika) + ") "
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
            

            if (hasError == False):
                form_errors.remove("----------------FINANSIJSKI IZVEŠTAJ FOND5----------------")
           
            if (hasWarning == False):
                form_warnings.remove("----------------FINANSIJSKI IZVEŠTAJ FOND5----------------")                
                
        #############################################
        ####             KRAJ FONDOVA          ######
        #############################################
        
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg,'trace':trace})

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}