import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'BANKE_9_STATISTICKI_IZVESTAJ_2021',
  templateUrl: 'BANKE_9_STATISTICKI_IZVESTAJ_2021.component.html',
})
export class BANKE_9_STATISTICKI_IZVESTAJ_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
