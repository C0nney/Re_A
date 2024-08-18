Java.perform(function() {
    var signature = Java.use("android.content.pm.Signature");

    signature.hashCode.implementation = function() {
        console.log('enter signature.hashCode');
        //printstack(); 
        return this.hashCode();
    };

    signature.toByteArray.implementation = function() {
        console.log('enter signature.toByteArray');
        //printstack(); 
        return this.toByteArray();
    };

    signature.equals.overload('java.lang.Object').implementation = function(obj) {
        console.log('enter signature.equals');
        //printstack(); 
        return this.equals(obj);
    };

    function printstack() {
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
    }
});


