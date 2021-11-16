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
        bs = getForme(Zahtev,'Bilans stanja')
        if len(bs)==0:
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Bilans stanja nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        bu = getForme(Zahtev,'Bilans uspeha')
        if len(bu)==0:
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Bilans uspeha nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        iotg = getForme(Zahtev,'Izveštaj o tokovima gotovine')
        if len(iotg)==0:
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Izveštaj o tokovima gotovine nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
      
        iopn = getForme(Zahtev,'Izveštaj o promenama neto imovine') #novi obrazac Izveštaj o promenama neto imovine
        if len(iopn)==0:
            naziv_obrasca='Obrazac'
            poruka  ='Izveštaj o promenama neto imovine nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        si = getForme(Zahtev,'Statistički izveštaj')
        if len(si)==0:
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Statistički izveštaj nije popunjen'
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
        if not( suma(bs,1,21,5)+suma(bs,1,21,6)+suma(bs,401,416,5)+suma(bs,401,416,6)+suma(bu,1001,1039,5)+suma(bu,1001,1039,6)+suma(iotg,3001,3031,3)+suma(iotg,3001,3031,4)+suma(iopn,4001,4018,4)+suma(iopn,4001,4018,5)+suma(si,9004,9018,4)+suma(si,9004,9018,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0021) kol. 5 + (0001 do 0021) kol. 6 bilansa stanja + (0401 do 0416) kol. 5 + (0401 do 0416) kol. 6 bilansa stanja + (1001 do 1039) kol. 5 + (1001 do 1039) kol. 6 bilansa uspeha + (3001 do 3031) kol. 3 + (3001 do 3031) kol. 4 izveštaja o tokovima gotovine + (4001 do 4018) kol. 4 + (4001 do 4018) kol. 5 izveštaja o promenama na neto imovini + (9004 do 9018) kol. 4 + (9004 do 9018) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0021) kol. 5 + (0001 do 0021) kol. 6 bilansa stanja + (0401 do 0416) kol. 5 + (0401 do 0416) kol. 6 bilansa stanja + (1001 do 1039) kol. 5 + (1001 do 1039) kol. 6 bilansa uspeha + (3001 do 3031) kol. 3 + (3001 do 3031) kol. 4 izveštaja o tokovima gotovine + (4001 do 4018) kol. 4 + (4001 do 4018) kol. 5 izveštaja o promenama na neto imovini + (9004 do 9018) kol. 4 + (9004 do 9018) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0021) kol. 5 + (0001 do 0021) kol. 6 bilansa stanja + (0401 do 0416) kol. 5 + (0401 do 0416) kol. 6 bilansa stanja + (1001 do 1039) kol. 5 + (1001 do 1039) kol. 6 bilansa uspeha + (3001 do 3031) kol. 3 + (3001 do 3031) kol. 4 izveštaja o tokovima gotovine + (4001 do 4018) kol. 4 + (4001 do 4018) kol. 5 izveštaja o promenama na neto imovini + (9004 do 9018) kol. 4 + (9004 do 9018) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0021) kol. 5 + (0001 do 0021) kol. 6 bilansa stanja + (0401 do 0416) kol. 5 + (0401 do 0416) kol. 6 bilansa stanja + (1001 do 1039) kol. 5 + (1001 do 1039) kol. 6 bilansa uspeha + (3001 do 3031) kol. 3 + (3001 do 3031) kol. 4 izveštaja o tokovima gotovine + (4001 do 4018) kol. 4 + (4001 do 4018) kol. 5 izveštaja o promenama na neto imovini + (9004 do 9018) kol. 4 + (9004 do 9018) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0021) kol. 5 + (0001 do 0021) kol. 6 bilansa stanja + (0401 do 0416) kol. 5 + (0401 do 0416) kol. 6 bilansa stanja + (1001 do 1039) kol. 5 + (1001 do 1039) kol. 6 bilansa uspeha + (3001 do 3031) kol. 3 + (3001 do 3031) kol. 4 izveštaja o tokovima gotovine + (4001 do 4018) kol. 4 + (4001 do 4018) kol. 5 izveštaja o promenama na neto imovini + (9004 do 9018) kol. 4 + (9004 do 9018) kol. 5 statističkog izveštaja > 0 Finansijski izveštaj ne sme biti bez podataka'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        #00000-2
        # U bar jednoj od tri navedene forme kolona napomena mora da ima bar jedan karakter
        bsNapomene = Zahtev.Forme['Bilans stanja'].TekstualnaPoljaForme;
        buNapomene = Zahtev.Forme['Bilans uspeha'].TekstualnaPoljaForme;
        iopnNapomene = Zahtev.Forme['Izveštaj o promenama neto imovine'].TekstualnaPoljaForme;
        
        if not( proveriNapomene(bsNapomene, 1, 21, 4) or proveriNapomene(bsNapomene, 401, 416, 4) or proveriNapomene(buNapomene, 1001, 1039, 4) or proveriNapomene(iopnNapomene, 4001, 4018, 3) ): 
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Na AOP-u (0001 do 0021) bilansa stanja + (0401 do 0416) bilansa stanja + (1001 do 1039) bilansa uspeha u koloni 4 i na AOP-u (4001 do 4018) izveštaja o promenama na neto imovini u koloni 3 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 i kolonu 3, u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Na AOP-u (0001 do 0021) bilansa stanja + (0401 do 0416) bilansa stanja + (1001 do 1039) bilansa uspeha u koloni 4 i na AOP-u (4001 do 4018) izveštaja o promenama na neto imovini u koloni 3 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 i kolonu 3, u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='Na AOP-u (0001 do 0021) bilansa stanja + (0401 do 0416) bilansa stanja + (1001 do 1039) bilansa uspeha u koloni 4 i na AOP-u (4001 do 4018) izveštaja o promenama na neto imovini u koloni 3 (Napomena) mora biti unet bar jedan karakter Potrebno je popuniti kolonu 4 i kolonu 3, u skladu sa oznakama iz Napomena uz finansijske izveštaje'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 416, 5, 6)
        lista_bu = find_negativni(bu, 1001, 1039, 5, 6)
        lista_iotg = find_negativni(iotg, 3001, 3031, 3, 4)
        lista_iopn = find_negativni(iopn, 4001, 4018, 4, 5)#koja je prva koja je poslednja kolona
        lista_si = find_negativni(si, 9001, 9018, 4, 5)

        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        
        if len(lista_iotg) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iotg
            else:
                lista = lista_iotg
        if len(lista_iopn) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_iopn
            else:
                lista = lista_iopn
        
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
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,21,5)+suma(bs,401,416,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0021) kol. 5 + (0401 do 0416) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,21,6)+suma(bs,401,416,6) == 0 ):
                lzbir =  suma(bs,1,21,6)+suma(bs,401,416,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0021) kol. 6 + (0401 do 0416) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,21,6)+suma(bs,401,416,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0021) kol. 6 + (0401 do 0416)  kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00004
        if not( aop(bs,1,5) == suma_liste(bs,[2,3,7],5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[2,3,7],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u (0002 + 0003 + 0007) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00005
        if not( aop(bs,1,6) == suma_liste(bs,[2,3,7],6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[2,3,7],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u (0002 + 0003 + 0007) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,3,5) == suma(bs,4,6,5) ):
            lzbir =  aop(bs,3,5) 
            dzbir =  suma(bs,4,6,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 5 = AOP-u (0004 + 0005 + 0006) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,3,6) == suma(bs,4,6,6) ):
            lzbir =  aop(bs,3,6) 
            dzbir =  suma(bs,4,6,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 6  = AOP-u (0004 + 0005 + 0006) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,7,5) == suma_liste(bs,[8,11,14,17,18,19,20,21],5) ):
            lzbir =  aop(bs,7,5) 
            dzbir =  suma_liste(bs,[8,11,14,17,18,19,20,21],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0007 kol. 5 = AOP-u (0008 + 0011 + 0014 + 0017 + 0018 + 0019 + 0020 + 0021) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,7,6) == suma_liste(bs,[8,11,14,17,18,19,20,21],6) ):
            lzbir =  aop(bs,7,6) 
            dzbir =  suma_liste(bs,[8,11,14,17,18,19,20,21],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0007 kol. 6 = AOP-u (0008 + 0011 + 0014 + 0017 + 0018 + 0019 + 0020 + 0021) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,8,5) == suma(bs,9,10,5) ):
            lzbir =  aop(bs,8,5) 
            dzbir =  suma(bs,9,10,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0008 kol. 5  = AOP-u (0009 + 0010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,8,6) == suma(bs,9,10,6) ):
            lzbir =  aop(bs,8,6) 
            dzbir =  suma(bs,9,10,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0008 kol. 6  = AOP-u (0009 + 0010) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,11,5) == suma(bs,12,13,5) ):
            lzbir =  aop(bs,11,5) 
            dzbir =  suma(bs,12,13,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0011 kol. 5 = AOP-u (0012 + 0013) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,11,6) == suma(bs,12,13,6) ):
            lzbir =  aop(bs,11,6) 
            dzbir =  suma(bs,12,13,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0011 kol. 6 = AOP-u (0012 + 0013) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,14,5) == suma(bs,15,16,5) ):
            lzbir =  aop(bs,14,5) 
            dzbir =  suma(bs,15,16,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0014 kol. 5 = AOP-u (0015 + 0016) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,14,6) == suma(bs,15,16,6) ):
            lzbir =  aop(bs,14,6) 
            dzbir =  suma(bs,15,16,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0014 kol. 6 = AOP-u (0015 + 0016) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,401,5) == suma_liste(bs,[402,406,407,408],5) ):
            lzbir =  aop(bs,401,5) 
            dzbir =  suma_liste(bs,[402,406,407,408],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 5 = AOP-u (0402 + 0406 + 0407 + 0408) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,401,6) == suma_liste(bs,[402,406,407,408],6) ):
            lzbir =  aop(bs,401,6) 
            dzbir =  suma_liste(bs,[402,406,407,408],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0401 kol. 6 = AOP-u (0402 + 0406 + 0407 + 0408) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,402,5) == suma(bs,403,405,5) ):
            lzbir =  aop(bs,402,5) 
            dzbir =  suma(bs,403,405,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0402 kol. 5 = AOP-u (0403 + 0404 + 0405) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,402,6) == suma(bs,403,405,6) ):
            lzbir =  aop(bs,402,6) 
            dzbir =  suma(bs,403,405,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0402 kol. 6 = AOP-u (0403 + 0404 + 0405) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,409,5) == aop(bs,1,5)-aop(bs,401,5) ):
            lzbir =  aop(bs,409,5) 
            dzbir =  aop(bs,1,5)-aop(bs,401,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 5 = AOP-u (0001 - 0401) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,409,6) == aop(bs,1,6)-aop(bs,401,6) ):
            lzbir =  aop(bs,409,6) 
            dzbir =  aop(bs,1,6)-aop(bs,401,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 6 = AOP-u (0001 - 0401) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,409,5) == suma_liste(bs,[410,411,413],5)-suma_liste(bs,[412,414],5) ):
            lzbir =  aop(bs,409,5) 
            dzbir =  suma_liste(bs,[410,411,413],5)-suma_liste(bs,[412,414],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 5 = AOP-u (0410 + 0411 - 0412 + 0413 - 0414) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if not( aop(bs,409,6) == suma_liste(bs,[410,411,413],6)-suma_liste(bs,[412,414],6) ):
            lzbir =  aop(bs,409,6) 
            dzbir =  suma_liste(bs,[410,411,413],6)-suma_liste(bs,[412,414],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 6 = AOP-u (0410 + 0411 - 0412 + 0413 - 0414) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1039,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1039) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1039,6) == 0 ):
                lzbir =  suma(bu,1001,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1039) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1039,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1039) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1001,5) == suma(bu,1002,1006,5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma(bu,1002,1006,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1001,6) == suma(bu,1002,1006,6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma(bu,1002,1006,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1003 + 1004 + 1005 + 1006) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if not( aop(bu,1007,5) == suma(bu,1008,1011,5) ):
            lzbir =  aop(bu,1007,5) 
            dzbir =  suma(bu,1008,1011,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1007 kol. 5 = AOP-u (1008 + 1009 + 1010 + 1011) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10007
        if not( aop(bu,1007,6) == suma(bu,1008,1011,6) ):
            lzbir =  aop(bu,1007,6) 
            dzbir =  suma(bu,1008,1011,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1007 kol. 6 = AOP-u (1008 + 1009 + 1010 + 1011) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if not( aop(bu,1012,5) == suma(bu,1013,1018,5) ):
            lzbir =  aop(bu,1012,5) 
            dzbir =  suma(bu,1013,1018,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1012 kol. 5 = AOP-u (1013 + 1014 + 1015 + 1016 + 1017 + 1018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10009
        if not( aop(bu,1012,6) == suma(bu,1013,1018,6) ):
            lzbir =  aop(bu,1012,6) 
            dzbir =  suma(bu,1013,1018,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1012 kol. 6 = AOP-u (1013 + 1014 + 1015 + 1016 + 1017 + 1018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10010
        if not( aop(bu,1019,5) == suma(bu,1020,1023,5) ):
            lzbir =  aop(bu,1019,5) 
            dzbir =  suma(bu,1020,1023,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1019 kol. 5 = AOP-u (1020 + 1021 + 1022 + 1023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10011
        if not( aop(bu,1019,6) == suma(bu,1020,1023,6) ):
            lzbir =  aop(bu,1019,6) 
            dzbir =  suma(bu,1020,1023,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1019 kol. 6 = AOP-u (1020 + 1021 + 1022 + 1023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10012
        if( suma_liste(bu,[1001,1007],5) > suma_liste(bu,[1012,1019],5) ):
            if not( aop(bu,1024,5) == suma_liste(bu,[1001,1007],5)-suma_liste(bu,[1012,1019],5) ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  suma_liste(bu,[1001,1007],5)-suma_liste(bu,[1012,1019],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1024 kol. 5 = AOP-u (1001 + 1007 - 1012 - 1019) kol. 5, ako je AOP (1001 + 1007) kol. 5 > AOP-a (1012 + 1019) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( suma_liste(bu,[1001,1007],6) > suma_liste(bu,[1012,1019],6) ):
            if not( aop(bu,1024,6) == suma_liste(bu,[1001,1007],6)-suma_liste(bu,[1012,1019],6) ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  suma_liste(bu,[1001,1007],6)-suma_liste(bu,[1012,1019],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1024 kol. 6 = AOP-u (1001 + 1007 - 1012 - 1019) kol. 6, ako je AOP (1001 + 1007) kol. 6 > AOP-a (1012 + 1019) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( suma_liste(bu,[1001,1007],5) < suma_liste(bu,[1012,1019],5) ):
            if not( aop(bu,1025,5) == suma_liste(bu,[1012,1019],5)-suma_liste(bu,[1001,1007],5) ):
                lzbir =  aop(bu,1025,5) 
                dzbir =  suma_liste(bu,[1012,1019],5)-suma_liste(bu,[1001,1007],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1025 kol. 5 = AOP-u (1012 + 1019 - 1001 - 1007) kol. 5, ako je AOP (1001 + 1007) kol. 5 < AOP-a (1012 + 1019) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( suma_liste(bu,[1001,1007],6) < suma_liste(bu,[1012,1019],6) ):
            if not( aop(bu,1025,6) == suma_liste(bu,[1012,1019],6)-suma_liste(bu,[1001,1007],6) ):
                lzbir =  aop(bu,1025,6) 
                dzbir =  suma_liste(bu,[1012,1019],6)-suma_liste(bu,[1001,1007],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1025 kol. 6 = AOP-u (1012 + 1019 - 1001 - 1007) kol. 6, ako je AOP (1001 + 1007) kol. 6 < AOP-a (1012 + 1019) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if( suma_liste(bu,[1001,1007],5) == suma_liste(bu,[1012,1019],5) ):
            if not( suma(bu,1024,1025,5) == 0 ):
                lzbir =  suma(bu,1024,1025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1024 + 1025) kol. 5 = 0, ako je AOP (1001 + 1007) kol. 5 = AOP-u (1012 + 1019) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( suma_liste(bu,[1001,1007],6) == suma_liste(bu,[1012,1019],6) ):
            if not( suma(bu,1024,1025,6) == 0 ):
                lzbir =  suma(bu,1024,1025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1024 + 1025) kol. 6 = 0, ako je AOP (1001 + 1007) kol. 6 = AOP-u (1012 + 1019) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1024,5) > 0 ):
            if not( aop(bu,1025,5) == 0 ):
                lzbir =  aop(bu,1025,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1024 kol. 5 > 0, onda je AOP 1025 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1025,5) > 0 ):
            if not( aop(bu,1024,5) == 0 ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1025 kol. 5 > 0, onda je AOP 1024 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1024,6) > 0 ):
            if not( aop(bu,1025,6) == 0 ):
                lzbir =  aop(bu,1025,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1024 kol. 6 > 0, onda je AOP 1025 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1025,6) > 0 ):
            if not( aop(bu,1024,6) == 0 ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1025 kol. 6 > 0, onda je AOP 1024 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if not( suma_liste(bu,[1001,1007,1025],5) == suma_liste(bu,[1012,1019,1024],5) ):
            lzbir =  suma_liste(bu,[1001,1007,1025],5) 
            dzbir =  suma_liste(bu,[1012,1019,1024],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007 + 1025) kol. 5 = AOP-u (1012 + 1019 + 1024) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10023
        if not( suma_liste(bu,[1001,1007,1025],6) == suma_liste(bu,[1012,1019,1024],6) ):
            lzbir =  suma_liste(bu,[1001,1007,1025],6) 
            dzbir =  suma_liste(bu,[1012,1019,1024],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007 + 1025) kol. 6 = AOP-u (1012 + 1019 + 1024) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10024
        if not( aop(bu,1026,5) == suma(bu,1027,1030,5) ):
            lzbir =  aop(bu,1026,5) 
            dzbir =  suma(bu,1027,1030,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 5 = AOP-u (1027 + 1028 + 1029 + 1030) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10025
        if not( aop(bu,1026,6) == suma(bu,1027,1030,6) ):
            lzbir =  aop(bu,1026,6) 
            dzbir =  suma(bu,1027,1030,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1026 kol. 6 = AOP-u (1027 + 1028 + 1029 + 1030) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10026
        if not( aop(bu,1031,5) == suma(bu,1032,1035,5) ):
            lzbir =  aop(bu,1031,5) 
            dzbir =  suma(bu,1032,1035,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1031 kol. 5 = AOP-u (1032 + 1033 + 1034 + 1035) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10027
        if not( aop(bu,1031,6) == suma(bu,1032,1035,6) ):
            lzbir =  aop(bu,1031,6) 
            dzbir =  suma(bu,1032,1035,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1031 kol. 6 = AOP-u (1032 + 1033 + 1034 + 1035) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1026,5) > aop(bu,1031,5) ):
            if not( aop(bu,1036,5) == aop(bu,1026,5)-aop(bu,1031,5) ):
                lzbir =  aop(bu,1036,5) 
                dzbir =  aop(bu,1026,5)-aop(bu,1031,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1036 kol. 5 = AOP-u (1026 - 1031) kol. 5 ako je AOP 1026 kol. 5 > AOP-a 1031 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1026,6) > aop(bu,1031,6) ):
            if not( aop(bu,1036,6) == aop(bu,1026,6)-aop(bu,1031,6) ):
                lzbir =  aop(bu,1036,6) 
                dzbir =  aop(bu,1026,6)-aop(bu,1031,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1036 kol. 6 = AOP-u (1026 - 1031) kol. 6 ako je AOP 1026 kol. 6 > AOP-a 1031 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1026,5) < aop(bu,1031,5) ):
            if not( aop(bu,1037,5) == aop(bu,1031,5)-aop(bu,1026,5) ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  aop(bu,1031,5)-aop(bu,1026,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 5 = AOP-u (1031 - 1026) kol. 5 ako je AOP 1026 kol. 5 < AOP-a 1031 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1026,6) < aop(bu,1031,6) ):
            if not( aop(bu,1037,6) == aop(bu,1031,6)-aop(bu,1026,6) ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  aop(bu,1031,6)-aop(bu,1026,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1037 kol. 6 = AOP-u (1031 - 1026) kol. 6 ako je AOP 1026 kol. 6 < AOP-a 1031 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1026,5) == aop(bu,1031,5) ):
            if not( suma(bu,1036,1037,5) == 0 ):
                lzbir =  suma(bu,1036,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1036 + 1037) kol. 5 = 0, ako je AOP 1026 kol. 5 = AOP-u 1031 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1026,6) == aop(bu,1031,6) ):
            if not( suma(bu,1036,1037,6) == 0 ):
                lzbir =  suma(bu,1036,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1036 + 1037) kol. 6 = 0, ako je AOP 1026 kol. 6 = AOP-u 1031 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1036,5) > 0 ):
            if not( aop(bu,1037,5) == 0 ):
                lzbir =  aop(bu,1037,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1036 kol. 5 > 0, onda je AOP 1037 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1037,5) > 0 ):
            if not( aop(bu,1036,5) == 0 ):
                lzbir =  aop(bu,1036,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 5 > 0, onda je AOP 1036 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1036,6) > 0 ):
            if not( aop(bu,1037,6) == 0 ):
                lzbir =  aop(bu,1037,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1036 kol. 6 > 0, onda je AOP 1037 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1037,6) > 0 ):
            if not( aop(bu,1036,6) == 0 ):
                lzbir =  aop(bu,1036,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1037 kol. 6 > 0, onda je AOP 1036 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if not( suma_liste(bu,[1026,1037],5) == suma_liste(bu,[1031,1036],5) ):
            lzbir =  suma_liste(bu,[1026,1037],5) 
            dzbir =  suma_liste(bu,[1031,1036],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1037) kol. 5 = AOP-u (1031 + 1036) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10039
        if not( suma_liste(bu,[1026,1037],6) == suma_liste(bu,[1031,1036],6) ):
            lzbir =  suma_liste(bu,[1026,1037],6) 
            dzbir =  suma_liste(bu,[1031,1036],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1037) kol. 6 = AOP-u (1031 + 1036) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10040
        if( suma_liste(bu,[1024,1036],5) > suma_liste(bu,[1025,1037],5) ):
            if not( aop(bu,1038,5) == suma_liste(bu,[1024,1036],5)-suma_liste(bu,[1025,1037],5) ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  suma_liste(bu,[1024,1036],5)-suma_liste(bu,[1025,1037],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 5 = AOP-u (1024 + 1036 - 1025 - 1037) kol. 5, ako je AOP (1024 + 1036) kol. 5 > AOP-a (1025 + 1037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( suma_liste(bu,[1024,1036],6) > suma_liste(bu,[1025,1037],6) ):
            if not( aop(bu,1038,6) == suma_liste(bu,[1024,1036],6)-suma_liste(bu,[1025,1037],6) ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  suma_liste(bu,[1024,1036],6)-suma_liste(bu,[1025,1037],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1038 kol. 6 = AOP-u (1024 + 1036 - 1025 - 1037) kol. 6, ako je AOP (1024 + 1036) kol. 6 > AOP-a (1025 + 1037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( suma_liste(bu,[1024,1036],5) < suma_liste(bu,[1025,1037],5) ):
            if not( aop(bu,1039,5) == suma_liste(bu,[1025,1037],5)-suma_liste(bu,[1024,1036],5) ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  suma_liste(bu,[1025,1037],5)-suma_liste(bu,[1024,1036],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 5 = AOP-u (1025 + 1037 - 1024 - 1036) kol. 5, ako je AOP (1024 + 1036) kol. 5 < AOP-a (1025 + 1037) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( suma_liste(bu,[1024,1036],6) < suma_liste(bu,[1025,1037],6) ):
            if not( aop(bu,1039,6) == suma_liste(bu,[1025,1037],6)-suma_liste(bu,[1024,1036],6) ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  suma_liste(bu,[1025,1037],6)-suma_liste(bu,[1024,1036],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1039 kol. 6 = AOP-u (1025 + 1037 - 1024 - 1036) kol. 6, ako je AOP (1024 + 1036) kol. 6 < AOP-a (1025 + 1037) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( suma_liste(bu,[1024,1036],5) == suma_liste(bu,[1025,1037],5) ):
            if not( suma(bu,1038,1039,5) == 0 ):
                lzbir =  suma(bu,1038,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1038 + 1039) kol. 5 = 0, ako je AOP (1024 + 1036) kol. 5 = AOP-u (1025 + 1037) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( suma_liste(bu,[1024,1036],6) == suma_liste(bu,[1025,1037],6) ):
            if not( suma(bu,1038,1039,6) == 0 ):
                lzbir =  suma(bu,1038,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1038 + 1039) kol. 6 = 0, ako je AOP (1024 + 1036) kol. 6 = AOP-u (1025 + 1037) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if( aop(bu,1038,5) > 0 ):
            if not( aop(bu,1039,5) == 0 ):
                lzbir =  aop(bu,1039,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 5 > 0, onda je AOP 1039 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( aop(bu,1039,5) > 0 ):
            if not( aop(bu,1038,5) == 0 ):
                lzbir =  aop(bu,1038,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 5 > 0, onda je AOP 1038 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1038,6) > 0 ):
            if not( aop(bu,1039,6) == 0 ):
                lzbir =  aop(bu,1039,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1038 kol. 6 > 0, onda je AOP 1039 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1039,6) > 0 ):
            if not( aop(bu,1038,6) == 0 ):
                lzbir =  aop(bu,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1039 kol. 6 > 0, onda je AOP 1038 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani povećanje i smanjenje neto imovine od poslovanja fonda '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if not( suma_liste(bu,[1024,1036,1039],5) == suma_liste(bu,[1025,1037,1038],5) ):
            lzbir =  suma_liste(bu,[1024,1036,1039],5) 
            dzbir =  suma_liste(bu,[1025,1037,1038],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1024 + 1036 + 1039) kol. 5 = AOP-u (1025 + 1037 + 1038) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10051
        if not( suma_liste(bu,[1024,1036,1039],6) == suma_liste(bu,[1025,1037,1038],6) ):
            lzbir =  suma_liste(bu,[1024,1036,1039],6) 
            dzbir =  suma_liste(bu,[1025,1037,1038],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1024 + 1036 + 1039) kol. 6 = AOP-u (1025 + 1037 + 1038) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10052
        #Za ovaj set se ne primenjuje pravilo 
        
        #10053
        #Za ovaj set se ne primenjuje pravilo 
        
        #10054
        #Za ovaj set se ne primenjuje pravilo 
        
        #10055
        #Za ovaj set se ne primenjuje pravilo 
        
        #IZVEŠTAJ O TOKOVIMA GOTOVINE - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #30001
        if not( suma(iotg,3001,3031,3) > 0 ):
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='Zbir podataka na oznakama za AOP (3001 do 3031) kol. 3 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za tekući izveštajni period;Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iotg,3001,3031,4) == 0 ):
                lzbir =  suma(iotg,3001,3031,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3031) kol. 4 = 0 Izveštaj o tokovima gotovine za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iotg,3001,3031,4) > 0 ):
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Zbir podataka na oznakama za AOP (3001 do 3031) kol. 4 > 0 Izveštaj o tokovima gotovine, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
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
        if not( aop(iotg,3006,3) == suma(iotg,3007,3013,3) ):
            lzbir =  aop(iotg,3006,3) 
            dzbir =  suma(iotg,3007,3013,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 3 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30007
        if not( aop(iotg,3006,4) == suma(iotg,3007,3013,4) ):
            lzbir =  aop(iotg,3006,4) 
            dzbir =  suma(iotg,3007,3013,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3006 kol. 4 = AOP-u (3007 + 3008 + 3009 + 3010 + 3011 + 3012 + 3013) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30008
        if( aop(iotg,3001,3) > aop(iotg,3006,3) ):
            if not( aop(iotg,3014,3) == aop(iotg,3001,3)-aop(iotg,3006,3) ):
                lzbir =  aop(iotg,3014,3) 
                dzbir =  aop(iotg,3001,3)-aop(iotg,3006,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 3 = AOP-u (3001 - 3006) kol. 3, ako je AOP 3001 kol. 3 > AOP-a 3006 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30009
        if( aop(iotg,3001,4) > aop(iotg,3006,4) ):
            if not( aop(iotg,3014,4) == aop(iotg,3001,4)-aop(iotg,3006,4) ):
                lzbir =  aop(iotg,3014,4) 
                dzbir =  aop(iotg,3001,4)-aop(iotg,3006,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3014 kol. 4 = AOP-u (3001 - 3006) kol. 4 ako je AOP 3001 kol. 4 > AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30010
        if( aop(iotg,3001,3) < aop(iotg,3006,3) ):
            if not( aop(iotg,3015,3) == aop(iotg,3006,3)-aop(iotg,3001,3) ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  aop(iotg,3006,3)-aop(iotg,3001,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 3 = AOP-u (3006 - 3001) kol. 3, ako je AOP 3001 kol. 3 < AOP-a 3006 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30011
        if( aop(iotg,3001,4) < aop(iotg,3006,4) ):
            if not( aop(iotg,3015,4) == aop(iotg,3006,4)-aop(iotg,3001,4) ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  aop(iotg,3006,4)-aop(iotg,3001,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3015 kol. 4 = AOP-u (3006 - 3001) kol. 4, ako je AOP 3001 kol. 4 < AOP-a 3006 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30012
        if( aop(iotg,3001,3) == aop(iotg,3006,3) ):
            if not( suma(iotg,3014,3015,3) == 0 ):
                lzbir =  suma(iotg,3014,3015,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3014 + 3015) kol. 3 = 0, ako je AOP 3001 kol. 3 = AOP-u 3006 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30013
        if( aop(iotg,3001,4) == aop(iotg,3006,4) ):
            if not( suma(iotg,3014,3015,4) == 0 ):
                lzbir =  suma(iotg,3014,3015,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3014 + 3015) kol. 4 = 0, ako je AOP 3001 kol. 4 = AOP-u 3006 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30014
        if( aop(iotg,3014,3) > 0 ):
            if not( aop(iotg,3015,3) == 0 ):
                lzbir =  aop(iotg,3015,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 3 > 0, onda je AOP 3015 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30015
        if( aop(iotg,3015,3) > 0 ):
            if not( aop(iotg,3014,3) == 0 ):
                lzbir =  aop(iotg,3014,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 3 > 0, onda je AOP 3014 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30016
        if( aop(iotg,3014,4) > 0 ):
            if not( aop(iotg,3015,4) == 0 ):
                lzbir =  aop(iotg,3015,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3014 kol. 4 > 0, onda je AOP 3015 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30017
        if( aop(iotg,3015,4) > 0 ):
            if not( aop(iotg,3014,4) == 0 ):
                lzbir =  aop(iotg,3014,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3015 kol. 4 > 0, onda je AOP 3014 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30018
        if not( suma_liste(iotg,[3001,3015],3) == suma_liste(iotg,[3006,3014],3) ):
            lzbir =  suma_liste(iotg,[3001,3015],3) 
            dzbir =  suma_liste(iotg,[3006,3014],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3015) kol. 3 = AOP-u (3006 + 3014) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30019
        if not( suma_liste(iotg,[3001,3015],4) == suma_liste(iotg,[3006,3014],4) ):
            lzbir =  suma_liste(iotg,[3001,3015],4) 
            dzbir =  suma_liste(iotg,[3006,3014],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3001 + 3015) kol. 4 = AOP-u (3006 + 3014) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30020
        if not( aop(iotg,3016,3) == suma(iotg,3017,3019,3) ):
            lzbir =  aop(iotg,3016,3) 
            dzbir =  suma(iotg,3017,3019,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3016 kol. 3 = AOP-u (3017 + 3018 + 3019) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30021
        if not( aop(iotg,3016,4) == suma(iotg,3017,3019,4) ):
            lzbir =  aop(iotg,3016,4) 
            dzbir =  suma(iotg,3017,3019,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3016 kol. 4 = AOP-u (3017 + 3018 + 3019) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30022
        if not( aop(iotg,3020,3) == suma(iotg,3021,3023,3) ):
            lzbir =  aop(iotg,3020,3) 
            dzbir =  suma(iotg,3021,3023,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3020 kol. 3 = AOP-u (3021 + 3022 + 3023) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30023
        if not( aop(iotg,3020,4) == suma(iotg,3021,3023,4) ):
            lzbir =  aop(iotg,3020,4) 
            dzbir =  suma(iotg,3021,3023,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3020 kol. 4 = AOP-u (3021 + 3022 + 3023) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30024
        if( aop(iotg,3016,3) > aop(iotg,3020,3) ):
            if not( aop(iotg,3024,3) == aop(iotg,3016,3)-aop(iotg,3020,3) ):
                lzbir =  aop(iotg,3024,3) 
                dzbir =  aop(iotg,3016,3)-aop(iotg,3020,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3024 kol. 3 = AOP-u (3016 - 3020) kol. 3, ako je AOP 3016 kol. 3 > AOP-a 3020 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30025
        if( aop(iotg,3016,4) > aop(iotg,3020,4) ):
            if not( aop(iotg,3024,4) == aop(iotg,3016,4)-aop(iotg,3020,4) ):
                lzbir =  aop(iotg,3024,4) 
                dzbir =  aop(iotg,3016,4)-aop(iotg,3020,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3024 kol. 4 = AOP-u (3016 - 3020) kol. 4, ako je AOP 3016 kol. 4 > AOP-a 3020 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30026
        if( aop(iotg,3016,3) < aop(iotg,3020,3) ):
            if not( aop(iotg,3025,3) == aop(iotg,3020,3)-aop(iotg,3016,3) ):
                lzbir =  aop(iotg,3025,3) 
                dzbir =  aop(iotg,3020,3)-aop(iotg,3016,3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3025 kol. 3 = AOP-u (3020 - 3016) kol. 3, ako je AOP 3016 kol. 3 < AOP-a 3020 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30027
        if( aop(iotg,3016,4) < aop(iotg,3020,4) ):
            if not( aop(iotg,3025,4) == aop(iotg,3020,4)-aop(iotg,3016,4) ):
                lzbir =  aop(iotg,3025,4) 
                dzbir =  aop(iotg,3020,4)-aop(iotg,3016,4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3025 kol. 4 = AOP-u (3020 - 3016) kol. 4, ako je AOP 3016 kol. 4 < AOP-a 3020 kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30028
        if( aop(iotg,3016,3) == aop(iotg,3020,3) ):
            if not( suma(iotg,3024,3025,3) == 0 ):
                lzbir =  suma(iotg,3024,3025,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3024 + 3025) kol. 3 = 0, ako je AOP 3016 kol. 3 = AOP-u 3020 kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30029
        if( aop(iotg,3016,4) == aop(iotg,3020,4) ):
            if not( suma(iotg,3024,3025,4) == 0 ):
                lzbir =  suma(iotg,3024,3025,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3024 + 3025) kol. 4 = 0, ako je AOP 3016 kol. 4 = AOP-u 3020 kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30030
        if( aop(iotg,3024,3) > 0 ):
            if not( aop(iotg,3025,3) == 0 ):
                lzbir =  aop(iotg,3025,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3024 kol. 3 > 0, onda je AOP 3025 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30031
        if( aop(iotg,3025,3) > 0 ):
            if not( aop(iotg,3024,3) == 0 ):
                lzbir =  aop(iotg,3024,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3025 kol. 3 > 0, onda je AOP 3024 kol. 3 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30032
        if( aop(iotg,3024,4) > 0 ):
            if not( aop(iotg,3025,4) == 0 ):
                lzbir =  aop(iotg,3025,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3024 kol. 4 > 0, onda je AOP 3025 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30033
        if( aop(iotg,3025,4) > 0 ):
            if not( aop(iotg,3024,4) == 0 ):
                lzbir =  aop(iotg,3024,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='Ako je AOP 3025 kol. 4 > 0, onda je AOP 3024 kol. 4 = 0 U Izveštaju o tokovima gotovine ne mogu biti istovremeno prikazani neto prilivi i odlivi '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30034
        if not( suma_liste(iotg,[3016,3025],3) == suma_liste(iotg,[3020,3024],3) ):
            lzbir =  suma_liste(iotg,[3016,3025],3) 
            dzbir =  suma_liste(iotg,[3020,3024],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3025) kol. 3 = AOP-u (3020 + 3024) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30035
        if not( suma_liste(iotg,[3016,3025],4) == suma_liste(iotg,[3020,3024],4) ):
            lzbir =  suma_liste(iotg,[3016,3025],4) 
            dzbir =  suma_liste(iotg,[3020,3024],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3016 + 3025) kol. 4 = AOP-u (3020 + 3024) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30036
        if( suma_liste(iotg,[3014,3024],3) > suma_liste(iotg,[3015,3025],3) ):
            if not( aop(iotg,3026,3) == suma_liste(iotg,[3014,3024],3)-suma_liste(iotg,[3015,3025],3) ):
                lzbir =  aop(iotg,3026,3) 
                dzbir =  suma_liste(iotg,[3014,3024],3)-suma_liste(iotg,[3015,3025],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 3 = AOP-u (3014 + 3024 - 3015 - 3025) kol. 3, ako je AOP (3014 + 3024) kol. 3 > AOP-a (3015 + 3025) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30037
        if( suma_liste(iotg,[3014,3024],4) > suma_liste(iotg,[3015,3025],4) ):
            if not( aop(iotg,3026,4) == suma_liste(iotg,[3014,3024],4)-suma_liste(iotg,[3015,3025],4) ):
                lzbir =  aop(iotg,3026,4) 
                dzbir =  suma_liste(iotg,[3014,3024],4)-suma_liste(iotg,[3015,3025],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3026 kol. 4 = AOP-u (3014 + 3024 - 3015 - 3025) kol. 4, ako je AOP (3014 + 3024) kol. 4 >  AOP-a (3015 + 3025) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30038
        if( suma_liste(iotg,[3014,3024],3) < suma_liste(iotg,[3015,3025],3) ):
            if not( aop(iotg,3027,3) == suma_liste(iotg,[3015,3025],3)-suma_liste(iotg,[3014,3024],3) ):
                lzbir =  aop(iotg,3027,3) 
                dzbir =  suma_liste(iotg,[3015,3025],3)-suma_liste(iotg,[3014,3024],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 3 = AOP-u (3015 + 3025 - 3014 - 3024) kol. 3,  ako je AOP (3014 + 3024) kol. 3 < AOP-a (3015 + 3025) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30039
        if( suma_liste(iotg,[3014,3024],4) < suma_liste(iotg,[3015,3025],4) ):
            if not( aop(iotg,3027,4) == suma_liste(iotg,[3015,3025],4)-suma_liste(iotg,[3014,3024],4) ):
                lzbir =  aop(iotg,3027,4) 
                dzbir =  suma_liste(iotg,[3015,3025],4)-suma_liste(iotg,[3014,3024],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3027 kol. 4 = AOP-u (3015 + 3025 - 3014 - 3024) kol. 4,  ako je AOP (3014 + 3024) kol. 4 < AOP-a (3015 + 3025) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30040
        if( suma_liste(iotg,[3014,3024],3) == suma_liste(iotg,[3015,3025],3) ):
            if not( suma(iotg,3026,3027,3) == 0 ):
                lzbir =  suma(iotg,3026,3027,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3026 + 3027) kol. 3 = 0, ako je AOP (3014 + 3024) kol. 3 = AOP-u (3015 + 3025) kol. 3 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30041
        if( suma_liste(iotg,[3014,3024],4) == suma_liste(iotg,[3015,3025],4) ):
            if not( suma(iotg,3026,3027,4) == 0 ):
                lzbir =  suma(iotg,3026,3027,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP (3026 + 3027) kol. 4 = 0, ako je AOP (3014 + 3024) kol. 4 = AOP-u (3015 + 3025) kol. 4 Rezultat mora biti jednak 0 ukoliko su prilivi i odlivi međusobno jednaki '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30042
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
        
        #30043
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
        
        #30044
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
        
        #30045
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
        
        #30046
        if not( suma_liste(iotg,[3014,3024,3027],3) == suma_liste(iotg,[3015,3025,3026],3) ):
            lzbir =  suma_liste(iotg,[3014,3024,3027],3) 
            dzbir =  suma_liste(iotg,[3015,3025,3026],3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3014 + 3024 + 3027) kol. 3 = AOP-u (3015 + 3025 + 3026) kol. 3 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30047
        if not( suma_liste(iotg,[3014,3024,3027],4) == suma_liste(iotg,[3015,3025,3026],4) ):
            lzbir =  suma_liste(iotg,[3014,3024,3027],4) 
            dzbir =  suma_liste(iotg,[3015,3025,3026],4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP (3014 + 3024 + 3027) kol. 4 = AOP-u (3015 + 3025 + 3026) kol. 4 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30048
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( aop(iotg,3028,3) == 0 ):
                lzbir =  aop(iotg,3028,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3028 kol. 3 = 0 Novoosnovani obveznici ne smeju imati prikazan podatak za prethodnu godinu '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30049
        if( suma_liste(iotg,[3026,3028,3029],3) > suma_liste(iotg,[3027,3030],3) ):
            if not( aop(iotg,3031,3) == suma_liste(iotg,[3026,3028,3029],3)-suma_liste(iotg,[3027,3030],3) ):
                lzbir =  aop(iotg,3031,3) 
                dzbir =  suma_liste(iotg,[3026,3028,3029],3)-suma_liste(iotg,[3027,3030],3) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3031 kol. 3 = AOP-u (3026 - 3027 + 3028 + 3029 - 3030) kol. 3, ako je AOP (3026 + 3028 + 3029) kol. 3 > AOP-a (3027 + 3030) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30050
        if( suma_liste(iotg,[3026,3028,3029],4) > suma_liste(iotg,[3027,3030],4) ):
            if not( aop(iotg,3031,4) == suma_liste(iotg,[3026,3028,3029],4)-suma_liste(iotg,[3027,3030],4) ):
                lzbir =  aop(iotg,3031,4) 
                dzbir =  suma_liste(iotg,[3026,3028,3029],4)-suma_liste(iotg,[3027,3030],4) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3031 kol. 4 = AOP-u (3026 - 3027 + 3028 + 3029 - 3030) kol. 4, ako je AOP (3026 + 3028 + 3029) kol. 4 > AOP-a (3027 + 3030) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30051
        if( suma_liste(iotg,[3026,3028,3029],3) <= suma_liste(iotg,[3027,3030],3) ):
            if not( aop(iotg,3031,3) == 0 ):
                lzbir =  aop(iotg,3031,3) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3031 kol. 3 = 0, ako je AOP (3026 + 3028 + 3029) kol. 3 ≤ AOP-a (3027 + 3030) kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30052
        if( suma_liste(iotg,[3026,3028,3029],4) <= suma_liste(iotg,[3027,3030],4) ):
            if not( aop(iotg,3031,4) == 0 ):
                lzbir =  aop(iotg,3031,4) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o tokovima gotovine'
                poruka  ='AOP 3031 kol. 4 = 0, ako je AOP (3026 + 3028 + 3029) kol. 4 ≤ AOP-a (3027 + 3030) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #30053
        if not( aop(iotg,3031,4) == aop(iotg,3028,3) ):
            lzbir =  aop(iotg,3031,4) 
            dzbir =  aop(iotg,3028,3) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3031 kol. 4 = AOP-u 3028 kol. 3  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #30054
        if not( aop(iotg,3031,3) == aop(bs,2,5) ):
            lzbir =  aop(iotg,3031,3) 
            dzbir =  aop(bs,2,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3031 kol. 3 = AOP-u 0002 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3031 kol. 3 = AOP-u 0002 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #30055
        if not( aop(iotg,3031,4) == aop(bs,2,6) ):
            lzbir =  aop(iotg,3031,4) 
            dzbir =  aop(bs,2,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 3031 kol. 4 = AOP-u 0002 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o tokovima gotovine'
            poruka  ='AOP 3031 kol. 4 = AOP-u 0002 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        
        #Izveštaj o promenama neto imovine - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #40001
        if not( suma(iopn,4001,4018,4) > 0 ):
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) kol. 4 > 0 izveštaj o promenama na neto imovini, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(iopn,4001,4018,5) == 0 ):
                lzbir =  suma(iopn,4001,4018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Izveštaj o promenama neto imovine'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) kol. 5 = 0 izveštaj o promenama na neto imovini za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #40003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(iopn,4001,4018,5) > 0 ):
                
                naziv_obrasca='Izveštaj o promenama neto imovine'
                poruka  ='Zbir podataka na oznakama za AOP (4001 do 4018) kol. 5 > 0 izveštaj o promenama na neto imovini, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #40004
        if not( aop(iopn,4002,4) == suma(iopn,4003,4009,4) ):
            lzbir =  aop(iopn,4002,4) 
            dzbir =  suma(iopn,4003,4009,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4002 kol. 4 = AOP-u (4003 + 4004 + 4005 + 4006 + 4007 + 4008 + 4009) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40005
        if not( aop(iopn,4002,5) == suma(iopn,4003,4009,5) ):
            lzbir =  aop(iopn,4002,5) 
            dzbir =  suma(iopn,4003,4009,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4002 kol. 5 = AOP-u (4003 + 4004 + 4005 + 4006 + 4007 + 4008 + 4009) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40006
        if not( aop(iopn,4010,4) == suma(iopn,4011,4017,4) ):
            lzbir =  aop(iopn,4010,4) 
            dzbir =  suma(iopn,4011,4017,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4010 kol. 4 = AOP-u (4011 + 4012 + 4013 + 4014 + 4015 + 4016 + 4017) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40007
        if not( aop(iopn,4010,5) == suma(iopn,4011,4017,5) ):
            lzbir =  aop(iopn,4010,5) 
            dzbir =  suma(iopn,4011,4017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4010 kol. 5 = AOP-u (4011 + 4012 + 4013 + 4014 + 4015 + 4016 + 4017) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40008
        if not( aop(iopn,4018,4) == suma(iopn,4001,4002,4)-aop(iopn,4010,4) ):
            lzbir =  aop(iopn,4018,4) 
            dzbir =  suma(iopn,4001,4002,4)-aop(iopn,4010,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4018 kol. 4 = AOP-u (4001 + 4002 - 4010) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40009
        if not( aop(iopn,4018,5) == suma(iopn,4001,4002,5)-aop(iopn,4010,5) ):
            lzbir =  aop(iopn,4018,5) 
            dzbir =  suma(iopn,4001,4002,5)-aop(iopn,4010,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4018 kol. 5 = AOP-u (4001 + 4002 - 4010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40010
        if not( aop(iopn,4018,5) == aop(iopn,4001,4) ):
            lzbir =  aop(iopn,4018,5) 
            dzbir =  aop(iopn,4001,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4018 kol. 5 = AOP-u 4001 kol. 4  Neto imovina na kraju perioda u koloni prethodna godina, po pravilu, mora biti jednaka neto imovini na početku perioda u koloni tekuća godina  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #40011
        if not( aop(iopn,4018,4) == aop(bs,409,5) ):
            lzbir =  aop(iopn,4018,4) 
            dzbir =  aop(bs,409,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4018 kol. 4 = AOP-u 0409 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4018 kol. 4 = AOP-u 0409 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #40012
        if not( aop(iopn,4018,5) == aop(bs,409,6) ):
            lzbir =  aop(iopn,4018,5) 
            dzbir =  aop(bs,409,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 4018 kol. 5 = AOP-u 0409 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Izveštaj o promenama neto imovine'
            poruka  ='AOP 4018 kol. 5 = AOP-u 0409 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #STATISTIČKI IZVEŠTAJ - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #90001
        if not( suma(si,9004,9018,4) > 0 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='Zbir podataka na oznakama za AOP (9004 do 9018) kol. 4 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90002
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(si,9004,9018,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9004 do 9018) kol. 5 > 0 Statistički izveštaj, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(si,9001,9003,4)+suma(si,9004,9018,5) == 0 ):
                lzbir =  suma(si,9001,9003,4)+suma(si,9004,9018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Zbir podataka na oznakama za AOP (9001 do 9003) kol. 4 + (9004 do 9018) kol. 5 = 0 Statistički izveštaj za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90004
        if not( 1 <= aop(si,9001,3) and aop(si,9001,3) <= 12 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 3 ≤ 12  Broj meseci poslovanja obveznika mora biti iskazan u intervalu između 1 i 12; '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90005
        if not( 1 <= aop(si,9001,4) and aop(si,9001,4) <= 12 ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='1 ≤ AOP-a 9001 kol. 4 ≤ 12  Broj meseci poslovanja obveznika osnovanih u ranijim godinama, po pravilu, mora biti iskazan u intervalu između 1 i 12; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #90006
        if not( aop(si,9003,3) <= aop(si,9002,3) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9003 kol. 3 ≤ AOP-a 9002 kol. 3  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90007
        if not( aop(si,9003,4) <= aop(si,9002,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9003 kol. 4 ≤ AOP-a 9002 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90008
        if( aop(si,9002,3) > 0 ):
            if not( aop(si,9005,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9002 kol. 3 > 0, onda je AOP 9005 kol. 4 > 0 Ukoliko u neto imovini fonda učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90009
        if( aop(si,9005,4) > 0 ):
            if not( aop(si,9002,3) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9005 kol. 4 > 0, onda je AOP 9002 kol. 3 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u neto imovini fonda; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90010
        if( aop(si,9002,4) > 0 ):
            if not( aop(si,9005,5) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9002 kol. 4 > 0, onda je AOP 9005 kol. 5 > 0 Ukoliko u neto imovini fonda učestvuju strana lica, mora biti iskazana vrednost stranog kapitala, ako je veća od 500,00 RSD; Ukoliko podaci o vrednosti kapitala nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje da je vrednost tog kapitala manja od 500,00 RSD '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #90011
        if( aop(si,9005,5) > 0 ):
            if not( aop(si,9002,4) > 0 ):
                
                naziv_obrasca='Statistički izveštaj'
                poruka  ='Ako je AOP 9005 kol. 5 > 0, onda je AOP 9002 kol. 4 > 0 Ukoliko je iskazana vrednost stranog kapitala, obveznik mora iskazati broj stranih lica koja učestvuju u neto imovini fonda; '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #90012
        if not( aop(si,9005,4) <= aop(si,9004,4) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 4 ≤ AOP-a 9004 kol. 4  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90013
        if not( aop(si,9005,5) <= aop(si,9004,5) ):
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9005 kol. 5 ≤ AOP-a 9004 kol. 5  '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90014
        if not( aop(si,9004,4) == aop(bs,410,5) ):
            lzbir =  aop(si,9004,4) 
            dzbir =  aop(bs,410,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9004 kol. 4 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 4 = AOP-u 0410 kol. 5 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90015
        if not( aop(si,9004,5) == aop(bs,410,6) ):
            lzbir =  aop(si,9004,5) 
            dzbir =  aop(bs,410,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 9004 kol. 5 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9004 kol. 5 = AOP-u 0410 kol. 6 bilansa stanja Kontrolno pravilo zahteva računsko slaganje istovrsnih podataka prikazanih u različitim obrascima u finansijskom izveštaju  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90016
        if not( aop(si,9009,4) == suma(si,9006,9008,4) ):
            lzbir =  aop(si,9009,4) 
            dzbir =  suma(si,9006,9008,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9009 kol. 4 = AOP-u (9006 + 9007 + 9008) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90017
        if not( aop(si,9009,5) == suma(si,9006,9008,5) ):
            lzbir =  aop(si,9009,5) 
            dzbir =  suma(si,9006,9008,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9009 kol. 5 = AOP-u (9006 + 9007 + 9008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90018
        if not( aop(si,9012,4) == suma(si,9010,9011,4) ):
            lzbir =  aop(si,9012,4) 
            dzbir =  suma(si,9010,9011,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 4 = AOP-u (9010 + 9011) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90019
        if not( aop(si,9012,5) == suma(si,9010,9011,5) ):
            lzbir =  aop(si,9012,5) 
            dzbir =  suma(si,9010,9011,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9012 kol. 5 = AOP-u (9010 + 9011) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90020
        if not( suma(si,9010,9011,4) <= aop(bu,1018,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9010 + 9011) kol. 4 ≤ AOP-a 1018 kol. 5 bilansa uspeha Troškovi poreza i premija osiguranja su izdvojeni deo Ostalih poslovnih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9010 + 9011) kol. 4 ≤ AOP-a 1018 kol. 5 bilansa uspeha Troškovi poreza i premija osiguranja su izdvojeni deo Ostalih poslovnih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90021
        if not( suma(si,9010,9011,5) <= aop(bu,1018,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9010 + 9011) kol. 5 ≤ AOP-a 1018 kol. 6 bilansa uspeha Troškovi poreza i premija osiguranja su izdvojeni deo Ostalih poslovnih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9010 + 9011) kol. 5 ≤ AOP-a 1018 kol. 6 bilansa uspeha Troškovi poreza i premija osiguranja su izdvojeni deo Ostalih poslovnih rashoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90022
        if not( aop(si,9018,4) == suma(si,9013,9017,4) ):
            lzbir =  aop(si,9018,4) 
            dzbir =  suma(si,9013,9017,4) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 4 = AOP-u (9013 + 9014 + 9015 + 9016 + 9017) kol. 4  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90023
        if not( aop(si,9018,5) == suma(si,9013,9017,5) ):
            lzbir =  aop(si,9018,5) 
            dzbir =  suma(si,9013,9017,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP 9018 kol. 5 = AOP-u (9013 + 9014 + 9015 + 9016 + 9017) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90024
        if not( suma(si,9013,9014,4) <= aop(bu,1002,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9013 + 9014) kol. 4 ≤ AOP-a 1002 kol. 5 bilansa uspeha Prihodi od kamata na depozite i na hartije od vrednosti su izdvojeni deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9013 + 9014) kol. 4 ≤ AOP-a 1002 kol. 5 bilansa uspeha Prihodi od kamata na depozite i na hartije od vrednosti su izdvojeni deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90025
        if not( suma(si,9013,9014,5) <= aop(bu,1002,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9013 + 9014) kol. 5 ≤ AOP-a 1002 kol. 6 bilansa uspeha Prihodi od kamata na depozite i na hartije od vrednosti su izdvojeni deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9013 + 9014) kol. 5 ≤ AOP-a 1002 kol. 6 bilansa uspeha Prihodi od kamata na depozite i na hartije od vrednosti su izdvojeni deo Prihoda od kamata '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90026
        if not( suma(si,9015,9017,4) <= aop(bu,1006,5) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9015 + 9016 + 9017) kol. 4 ≤ AOP-a 1006 kol. 5 bilansa uspeha Prihodi od naknada šteta od društva za osiguranje, od povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo Ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9015 + 9016 + 9017) kol. 4 ≤ AOP-a 1006 kol. 5 bilansa uspeha Prihodi od naknada šteta od društva za osiguranje, od povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo Ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #90027
        if not( suma(si,9015,9017,5) <= aop(bu,1006,6) ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (9015 + 9016 + 9017) kol. 5 ≤ AOP-a 1006 kol. 6 bilansa uspeha Prihodi od naknada šteta od društva za osiguranje, od povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo Ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Statistički izveštaj'
            poruka  ='AOP (9015 + 9016 + 9017) kol. 5 ≤ AOP-a 1006 kol. 6 bilansa uspeha Prihodi od naknada šteta od društva za osiguranje, od povraćaja poreskih dažbina i po osnovu donacija su izdvojeni deo Ostalih poslovnih prihoda '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #POSEBNI PODACI - NEMA
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}



